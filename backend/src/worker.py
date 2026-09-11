import json
from time import sleep
import requests
from pathlib import Path


from services import (
    get_token,
    build_metadata,
    tag_with_cover,
    format_song,
    clean_job,
)

from core import spotify
from services.yt_service import download_mp3
from core.files import FINISHED_DIR, JOBS_DIR, QUE_DIR
from services.file_service import read_file, rename_file
from services.spotify_service import get_metadata, get_music_cover
from services.ffmpeg_service import clean_spotify_data

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
