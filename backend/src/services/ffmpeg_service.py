import subprocess
from pathlib import Path


def build_metadata(track: dict):
    """Convert Spotify track data into repeated ffmpeg -metadata args."""
    artist = track["artists"][0]["name"]
    title = track["name"]
    album = track["album"]["name"]
    track_number = track["track_number"]
    date = track["release_date"]
    spotify_url = track["share_url"]

    return [
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album={album}",
        "-metadata", f"track={track_number}",
        "-metadata", f"date={date}",
        "-metadata", f"comment={spotify_url}",
    ]


def tag_with_cover(input_audio: str | Path, output_audio: str | Path, track: dict, cover: str| Path):
    """Combine audio + cover art + metadata into a finished MP3."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_audio,          # 1st input: audio
        "-i", cover,                # 2nd input: cover image
        "-map", "0:a",              # take audio stream from input 0
        "-map", "1:v",              # take image stream from input 1
        "-c:a", "copy",             # copy audio (no re-encode)
        "-c:v", "mjpeg",            # encode image as JPEG
        "-id3v2_version", "3",      # ID3 version that supports cover art
        "-metadata:s:v", "title=Album cover",
        "-metadata:s:v", "comment=Cover (front)",
        *build_metadata(track),     # spreads the -metadata flags
        output_audio,
    ]
    subprocess.run(cmd, check=True)
    return output_audio
