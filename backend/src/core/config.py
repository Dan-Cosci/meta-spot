import os

from dotenv import load_dotenv

load_dotenv(".env.local")

spotify_settings = {
    "client_id": str(os.getenv("spotify_client_id")),
    "client_secret": str(os.getenv("spotify_client_secret")),
    "token_api": str(os.getenv("spotify_token_api")),
    "api": str(os.getenv("spotify_api")),
}

api_settings = {
    "port": int(str(os.getenv("port"))),
    "host": str(os.getenv("host")),
    "env": str(os.getenv("env"))
}

thread_settings = {
    "max_que": int(str(os.getenv("max_que"))),
    "max_threads": int(str(os.getenv("max_threads")))
}
