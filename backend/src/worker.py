import threading
from datetime import datetime
from pathlib import Path
from queue import Queue
from time import sleep

from core import FINISHED_DIR, JOBS_DIR, api_settings, store
from models import JOB_STATUS
from services import (
    clean_job,
    clean_spotify_data,
    download_mp3,
    format_song,
    get_metadata,
    get_music_cover,
    tag_with_cover,
)


def process_job(task):
    for i in range(3):

        job_name = str(task.job_id)
        store.update_status(job_id=task.job_id, status=JOB_STATUS.PROCESSING)
        try:
            download_mp3(task)
            spotify_raw = get_metadata(task)
            spotify_data = clean_spotify_data(spotify_raw)

            song_name= format_song(spotify_data)
            art = get_music_cover(base=JOBS_DIR, file_name=job_name, track_data=spotify_data)
            tag_with_cover(
                cover=art,
                input_audio=Path(JOBS_DIR, f"{job_name}.mp3"),
                track=spotify_data,
                output_audio=Path(FINISHED_DIR, f"{song_name}_{job_name}.mp3")
            )

            updated_job = store.get(task.job_id)
            if not updated_job: return

            updated_job.file_name=str(song_name+".mp3")
            updated_job.file_path=FINISHED_DIR
            updated_job.downloaded_at=datetime.now().timestamp()
            updated_job.status=JOB_STATUS.DONE

            store.update_job(job_id=task.job_id, item=updated_job)

            for i in JOBS_DIR.glob(f"{job_name}.*"):
                clean_job(Path(JOBS_DIR,i))

            clean_job(Path(JOBS_DIR,job_name))
            break
        except Exception:
            print(f"failed downaload: {job_name}, attempt: {i + 1}")
            sleep(1)
            continue

def delete_worker(id: int, stop: threading.Event):
    while not stop.is_set():
        try:
            downloaded = store.list_downloaded()
            if not downloaded: continue
            for item in downloaded:
                job = store.get(item)
                if job is None or job.downloaded_at is None: continue

                if job.downloaded_at + api_settings["expires_in"] <= datetime.now().timestamp():
                    store.delete(item)
                    clean_job(job.file_path)
                    print(f"Clean process: Deleted {job.file_name}")

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
            store.init_job(job=task)
            process_job(task)

        except:
            print(f"Worker {id}: Failed to do task {task.job_id}")
