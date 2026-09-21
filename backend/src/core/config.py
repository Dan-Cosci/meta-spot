import os

from dotenv import load_dotenv

load_dotenv(".env.local")

spotify_settings = {
    "client_id": os.getenv("spotify_client_id", ""),
    "client_secret": os.getenv("spotify_client_secret", ""),
    "token_api": os.getenv("spotify_token_api", "https://accounts.spotify.com/api/token"),
    "api": os.getenv("spotify_api", "https://api.spotify.com/v1/"),
}

api_settings = {
    "port": int(os.getenv("port", "8080")),
    "host": os.getenv("host", "0.0.0.0"),
    "env": os.getenv("env", "development"),
    # Seconds a downloaded file is kept before the delete worker removes it.
    "expires_in": float(os.getenv("expires_in", "3600")),
}

cors_settings = {
    "allowed_methods": str(os.getenv("allowed_methods")).split(","),
    "allowed_origins": str(os.getenv("allowed_origins")).split(","),
}

thread_settings = {
    "max_que": int(os.getenv("max_que", "100")),
    "max_threads": int(os.getenv("max_threads", "3")),
}
