import json
from time import sleep
import requests
from pathlib import Path


from services import (
    tag_with_cover,
    format_song,
    download_mp3,
    get_metadata,
    get_music_cover,
    clean_spotify_data,
    read_file,
    rename_file,
)

from core import FINISHED_DIR, JOBS_DIR, QUE_DIR

print("running worker process")

while True:
    job_name = None
    for i in QUE_DIR.iterdir():
        print(i)
        try:
            file = rename_file(
                base=QUE_DIR,
                file_name=i.name,
                new_file_name=i.name,
                base2=JOBS_DIR
            )

            job_name = file.name
            break
        except FileNotFoundError:
            continue

    if not job_name:
        print("waiting for jobs...")
        sleep(2)
        continue

    for i in range(3):
        try:
            print(job_name)
            job_file = read_file(JOBS_DIR, job_name)
            download_mp3(job_file)
            spotify_raw = get_metadata(job_file)
            spotify_data = clean_spotify_data(spotify_raw)

            song_name= format_song(spotify_data)
            art = get_music_cover(base=JOBS_DIR, file_name=job_name, track_data=spotify_data)
            tag_with_cover(
                cover=art,
                input_audio=Path(JOBS_DIR, f"{job_name}.mp3"),
                track=spotify_data,
                output_audio=Path(FINISHED_DIR, f"{song_name}.mp3")
            )
            job_name = None
            break
        except Exception:
            print(f"failed downaload: {job_name}, attempt: {i+1}")
            sleep(1)
            continue
