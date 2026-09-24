import json
from pathlib import Path

import requests
from spotify_scraper import Track

from core import spotify_settings
from models import JOB_RESPONSE
from services.file_service import write_img
from core import client_store
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


def search_track(worker_id: int, q: str, types=("track",), limit=5 ):
    client = client_store.get(worker_id=worker_id)
    res = client.search(q, types=types, limit=limit)
    return res.to_dict()["tracks"][0]["id"]

def get_track_data(worker_id: int, track_id: str):
    client = client_store.get(worker_id=worker_id)
    return client.get_track(track_id).to_dict()

def get_music_cover(track_data: dict, file_name: Path | str, base: Path) -> Path:
    url = track_data["album"]["images"][0]["url"]
    r = requests.get(url)
    return write_img(base=base, file_name=file_name, data=r.content)
