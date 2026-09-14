from dotenv import load_dotenv
import os

load_dotenv(".env.local")

spotify_settings = {
    "client_id": str(os.getenv("spotify_client_id")),
    "client_secret": str(os.getenv("spotify_client_secret")),
    "token_api": str(os.getenv("spotify_token_api")),
    "api": str(os.getenv("spotify_api")),
}

api_settings = {
    "port": int(str(os.getenv("port"))),
    "host": str(os.getenv("host"))
}

thread_settings = {
    "max_que": int(str(os.getenv("max_que"))),
    "threads": int(str(os.getenv("threads")))
}
