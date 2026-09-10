# meta-spot

> **Name is a work in progress** — the project is currently called `meta-spot` and may be renamed later.

A music downloader that grabs audio with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and enriches it with metadata from the [Spotify Web API](https://developer.spotify.com/documentation/web-api). The result is a complete MP3 — proper title, artist, album, cover art, and tags — so it displays correctly in any music player.

## What it does

1. Searches for a song (or accepts a YouTube URL).
2. Downloads the audio with yt-dlp.
3. Fetches track metadata (title, artist, album, cover art, etc.) from Spotify.
4. Uses ffmpeg to convert the audio to MP3 and embed the metadata + album art.
5. Produces a finished, fully-tagged MP3 file.

## Requirements

- Python 3.13+
- [ffmpeg](https://ffmpeg.org/) installed and available on your `PATH`
- [uv](https://github.com/astral-sh/uv) (package manager)
- Spotify API credentials (client ID + secret)

## Setup

1. Clone the repository and enter the backend directory:

   ```sh
   cd backend
   ```

2. Install dependencies:

   ```sh
   uv sync
   ```

3. Create a `.env.local` file with your Spotify credentials:

   ```env
   spotify_client_id=your-client-id
   spotify_client_secret=your-client-secret
   spotify_token_api=https://accounts.spotify.com/api/token
   spotify_api=https://api.spotify.com/v1/
   ```

4. Run the application:

   ```sh
   uv run python src/main.py "Song Title"
   ```

## Status

🚧 **Work in progress** — this is an early-stage project. Features and structure may change.

## Disclaimer

This project is for educational purposes. Downloading music may violate the terms of service of the source platforms and copyright law in your jurisdiction. Use responsibly.
