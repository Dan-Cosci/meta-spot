from re import search
import threading
from pathlib import Path
from queue import Queue

from core import FINISHED_DIR, JOBS_DIR, job_store
from models import JOB_RESPONSE, JOB_STATUS
from services import (
    clean_job,
    download_mp3,
    get_track_data,
    get_music_cover,
    search_track,
    tag_with_cover,
)
from utils import get_current_timestamp, time_expires_in


def process_job(task: JOB_RESPONSE, worker_id: int):
    for i in range(3):

        job_name = str(task.job_id)
        job_store.update_status(job_id=task.job_id, status=JOB_STATUS.PROCESSING)
        try:
            track_id = search_track(worker_id, task.song)
            track = get_track_data(worker_id, track_id)

            task.song = f"{track["artists"][0]["name"]} - {track["name"]}"

            download_mp3(task)

            art = get_music_cover(base=JOBS_DIR, file_name=job_name, track_data=track)
            output_name = f"{task.song}_{task.job_id}.mp3"
            tag_with_cover(
                cover=art,
                input_audio=Path(JOBS_DIR, f"{task.job_id}.mp3"),
                track=track,
                output_audio=Path(FINISHED_DIR, output_name)
            )

            updated_job = job_store.get(task.job_id)
            if not updated_job: return

            updated_job.file_name=str(task.song+".mp3")
            updated_job.file_path=Path(FINISHED_DIR, output_name)
            updated_job.status=JOB_STATUS.DONE

            job_store.update_job(job_id=task.job_id, item=updated_job)

            for f in JOBS_DIR.glob(f"{job_name}.*"):
                clean_job(Path(JOBS_DIR,f))

            clean_job(Path(JOBS_DIR,job_name))
            break


        except Exception as e:
            print(f"failed downaload: {job_name}, attempt: {i + 1}\n\n error log: {e}")
            print()
            continue

    if job_store.get(task.job_id).status == JOB_STATUS.DONE: return
    job_store.update_status(task.job_id, JOB_STATUS.FAILED)
    raise Exception("Failed to download job")


def delete_worker(id: int, stop: threading.Event):
    while not stop.is_set():
        try:
            # checks for downloaded files
            downloaded = job_store.list_downloaded()
            if downloaded:
                for item in downloaded:
                    job = job_store.get(item)
                    if job is None or job.downloaded_at is None: continue

                    if time_expires_in(job.downloaded_at) <= get_current_timestamp():
                        clean_job(job.file_path)
                        job_store.delete(item)
                        print(f"Clean process: Deleted {job.file_name}")



            # checks for failed jobs in que
            failed = job_store.list_failed()
            if failed:
                for item in failed:
                    for i in JOBS_DIR.glob(f"{item}.*"): clean_job(i)
                    job_store.delete(item)
                    print(f"Clean process: Deleted failed job: {item}")


            done = job_store.list_done()
            if done:
                for item in done:
                    job = job_store.get(item)
                    if not job: continue

                    if time_expires_in(job.created_at) >= get_current_timestamp(): continue

                    for i in FINISHED_DIR.glob(f"*_{item}.*"): clean_job(i)
                    job_store.delete(item)
                    print(f"Clean process: Deleted jobs not downloaded: {item}")




        except Exception as e:
            print(f"Delete worker error: {e}")
            continue
        finally:
            stop.wait(timeout=30)



def worker(id: int, q: Queue, stop: threading.Event):
    while not stop.is_set():
        try:
            task = q.get(timeout=1.0)
            print(task)
        except:
            continue

        try:
            job_store.init_job(job=task)
            process_job(task, id)

        except:
            print(f"Worker {id}: Failed to do task {task.job_id}")
