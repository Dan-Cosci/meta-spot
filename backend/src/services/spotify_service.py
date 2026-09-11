from datetime import datetime
import requests
import json
from core import spotify
from pathlib import Path

from services.file_service import write_file, write_img

def get_token():

    if Path("token.json").exists():
        with open("token.json","r") as file:
            cur = json.load(file)
            if datetime.now().timestamp() < cur["expires_at"]:
                return cur["access_token"]

    data = {
        "grant_type": "client_credentials",
        "client_id": spotify["client_id"],
        "client_secret": spotify["client_secret"],
    }

    res = requests.post(spotify["token_api"], data=data).json()
    res["expires_at"] = datetime.now().timestamp() + res["expires_in"]
    with open("token.json", "w") as file: json.dump(res, file, indent=2)

    print("Requested new access token")
    return res["access_token"]

def get_metadata(job_file:dict):
    params = {
        "q": f"{job_file["song"]}",
        "type" : "track",
        "limit": 1
    }
    return requests.get(spotify["api"]+"search", params=params, headers={"Authorization": f"Bearer {get_token()}"}).json()

def get_music_cover(track_data: dict, file_name: Path, base: Path) -> Path:
    url = track_data["album"]["images"][0]["url"]
    r = requests.get(url)
    return write_img(base=base, file_name=file_name, data=r.content)
