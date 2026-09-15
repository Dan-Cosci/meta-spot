from yt_dlp import YoutubeDL

from core import JOBS_DIR
from models import JOB_RESPONSE


def download_mp3(job_file: JOB_RESPONSE):
    job_id = job_file.job_id
    song = job_file.song

    with YoutubeDL({
        "format": "bestaudio/best",
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        }],
        "outtmpl": f"{JOBS_DIR}/{job_id}.%(ext)s",
        "retries": 3
    }) as ydl:
        ydl.download(f"ytsearch1:{song} lyrics")
