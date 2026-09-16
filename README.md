# meta-spot

A self-hosted music downloader with a web interface. Search for a song, queue it, and get back a finished MP3 with the correct title, artist, album, cover art, and tags.

It combines three tools:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) downloads the audio.
- The [Spotify Web API](https://developer.spotify.com/documentation/web-api) supplies the metadata (title, artist, album, release date, cover art).
- [ffmpeg](https://ffmpeg.org/) converts the audio to MP3 and embeds the tags and artwork.

The result plays correctly in any music player.

## Features

- Search by song or artist name — no URL required.
- Live queue with per-song status (pending, processing, done, failed).
- One-click download of the finished MP3.
- Bulk queueing through the API (`POST /job/bulk`).
- Embedded metadata: title, artist, album, track number, release date, and cover art.
- Up to 3 retry attempts per song before a job is marked failed.

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python 3.13, FastAPI, Pydantic, yt-dlp, uvicorn |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Axios |
| Media | ffmpeg, Spotify Web API |
| Tooling | uv, npm |

## How it works

1. The browser sends a song request to the FastAPI backend.
2. The job gets an ID and is placed on an in-memory queue.
3. Three worker threads pull jobs off the queue and process them independently.
4. Each worker: downloads audio with yt-dlp → fetches metadata from Spotify → fetches the cover art → runs ffmpeg to embed tags and artwork → saves the finished MP3.
5. The frontend polls the job's status every 2 seconds and shows the download button when it's done.

The server and workers run in the same process and share a thread-safe job store (`backend/src/core/state.py`), so status updates are immediately visible to the API.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/job` | Queue one song |
| `POST` | `/job/bulk` | Queue many songs at once |
| `GET` | `/job/{job_id}` | Job details |
| `GET` | `/status/{job_id}` | Live job status |
| `GET` | `/download/{job_id}` | Download the finished MP3 |

## Requirements

- Python 3.13+
- Node.js 20+
- [ffmpeg](https://ffmpeg.org/) installed and available on your `PATH`
- [uv](https://github.com/astral-sh/uv) (backend package manager)
- Spotify API credentials (client ID + secret, free to create)

## Setup

### 1. Backend

```sh
cd backend
uv sync --frozen
```

Create `.env.local`:

```env
spotify_client_id=your-client-id
spotify_client_secret=your-client-secret
spotify_token_api=https://accounts.spotify.com/api/token
spotify_api=https://api.spotify.com/v1/
port=8000
host=127.0.0.1
env=development
max_que=100
max_threads=3
```

Run it:

```sh
uv run python src/main.py
```

### 2. Frontend

```sh
cd frontend
npm install
```

Create `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Run it:

```sh
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

## Project structure

```
backend/
  src/
    main.py        # FastAPI app, routes, starts the worker threads
    worker.py      # worker threads and the download/tag pipeline
    core/          # config, file paths, thread-safe job store
    models/        # Pydantic schemas and job status enum
    services/      # yt-dlp, Spotify, ffmpeg, file helpers
frontend/
  src/             # React UI (queue, status polling, download)
thread.py          # standalone threading experiment used to prototype the worker pool
```

## Known limitations

- The job queue lives in memory, so queued jobs are lost if the process restarts.
- The worker count is fixed at 3 in `main.py`; the `max_threads` setting exists but isn't wired up yet.
- Spotify token refresh isn't synchronized across threads, so concurrent jobs can occasionally request more than one token.
- Built to run locally or on a home server, not for public hosting.

## Status

🚧 **Work in progress** — features and structure may change.

## Disclaimer

This project is for educational and personal use. Downloading music may violate the terms of service of the source platforms and copyright law in your jurisdiction. Use responsibly.
