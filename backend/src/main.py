import json
from sys import argv
from yt_dlp import  YoutubeDL
import requests


from spotify_handler import get_token
from src.core import *

curr_dir = os.getcwd()
job_dir = curr_dir + "/src/temp/jobs/"

if len(argv) <= 1:
    print("requires song argument")
    exit(1)

with YoutubeDL({
    "format" : "bestaudio/best",
    "postprocessors" : [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',      # extract to mp3
        'preferredquality': '192',    # bitrate in kbps (optional)
    }],
    "outtmpl" : f"{job_dir}%(title)s.%(ext)s",
}) as ydl:
    fiel = ydl.download(f"ytsearch1:{argv[1]} lyrics")


songs = os.listdir(job_dir)
print(songs[0])

params = {
    "q": f"{argv[1]}",
    "type" : "track",
    "limit": 1
}
with open("out.json", "w") as file:
    data = requests.get(spotify_api+"search", params=params, headers={"Authorization": f"Bearer {get_token()}"}).json()
    json.dump(data, file, indent=2)

from ffmpeg_handler import *

track = load_spotify_track("out.json")
img_dest = download_cover(track=track)
meta = build_metadata(track)
output = "src/temp/finished/"+format_song(track)
tag_with_cover(input_audio=f"{job_dir}/{songs[0]}", output_audio=f"{output}.mp3", track=track, )

clean_job(f"src/temp/jobs/{songs[0]}")
