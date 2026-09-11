from dotenv import load_dotenv
import os

load_dotenv(".env.local")
client = str(os.getenv("spotify_client_id"))
secret = str(os.getenv("spotify_client_secret"))
token_api = str(os.getenv("spotify_token_api"))
spotify_api = str(os.getenv("spotify_api"))
