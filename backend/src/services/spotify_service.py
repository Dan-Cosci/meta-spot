import json
from datetime import datetime
from pathlib import Path

import requests

from core import spotify_settings
from models import JOB_RESPONSE
from services.file_service import write_img
from utils import get_current_timestamp


def get_token():

    if Path(".token").exists():
        with open(".token","r") as file:
            cur = json.load(file)
            if get_current_timestamp() < cur["expires_at"]:
                return cur["access_token"]

    data = {
        "grant_type": "client_credentials",
        "client_id": spotify_settings["client_id"],
        "client_secret": spotify_settings["client_secret"],
    }

    res = requests.post(spotify_settings["token_api"], data=data).json()
    res["expires_at"] = get_current_timestamp() + res["expires_in"]
    with open(".token", "w") as file: json.dump(res, file, indent=2)

    print("Requested new access token")
    return res["access_token"]

def get_metadata(job_file:JOB_RESPONSE):
    params = {
        "q": f"{job_file.song}",
        "type" : "track",
        "limit": 1
    }
    return requests.get(spotify_settings["api"]+"search", params=params, headers={"Authorization": f"Bearer {get_token()}"}).json()

def get_music_cover(track_data: dict, file_name: Path | str, base: Path) -> Path:
    url = track_data["album"]["images"][0]["url"]
    r = requests.get(url)
    return write_img(base=base, file_name=file_name, data=r.content)
