from yt_dlp import YoutubeDL

from core.files import JOBS_DIR


def download_mp3(job_file: dict):
    job_id = job_file["job_id"]
    song = job_file["song"]

    with YoutubeDL({
        "format": "bestaudio/best",
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        "outtmpl": f"{JOBS_DIR}/{job_id}.%(ext)s",
    }) as ydl:
        ydl.download(f"ytsearch1:{song} lyrics")
