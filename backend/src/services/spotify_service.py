from datetime import datetime
import requests
import json
from core import spotify
from pathlib import Path

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
