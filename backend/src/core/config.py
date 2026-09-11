from dotenv import load_dotenv
import os

load_dotenv(".env.local")

spotify = {
    "client_id": str(os.getenv("spotify_client_id")),
    "client_secret": str(os.getenv("spotify_client_secret")),
    "token_api": str(os.getenv("spotify_token_api")),
    "api": str(os.getenv("spotify_api")),
}

api = {

}
