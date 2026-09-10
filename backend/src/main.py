from datetime import datetime
import json
from sys import argv
from yt_dlp import  YoutubeDL
import requests
import os
from dotenv import load_dotenv

# env loader
load_dotenv(".env.local")
client = str(os.getenv("spotify_client_id"))
secret = str(os.getenv("spotify_client_secret"))
token_api = str(os.getenv("spotify_token_api"))
spotify_api = str(os.getenv("spotify_api"))

def get_token():

    if os.path.exists("token.json"):
        with open("token.json","r") as file:
            cur = json.load(file)
            if datetime.now().timestamp() < cur["expires_at"]:
                return cur["access_token"]

    data = {
        "grant_type": "client_credentials",
        "client_id": client,
        "client_secret": secret,
    }
    res = requests.post(token_api, data=data).json()
    res["expires_at"] = datetime.now().timestamp() + res["expires_in"]
    with open("token.json", "w") as file: json.dump(res, file, indent=2)

    print("Requested new access token")
    return res["access_token"]

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
