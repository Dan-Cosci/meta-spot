<div align="center">
  <img src="frontend/src/assets/meta-spot-dark.svg" alt="meta-spot" width="160" />
  <h1>meta-spot</h1>
  <p><b>A self-hosted music downloader with a web interface.</b></p>
  <p>Search or browse, queue a song, and get back a finished MP3 with the correct title, artist, album, track number, release date, and cover art.</p>
</div>

---

meta-spot combines three tools into one pipeline:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) downloads the audio.
- [spotify-scraper](https://pypi.org/project/spotifyscraper/) looks up the real metadata and cover art (no API keys required).
- [ffmpeg](https://ffmpeg.org/) converts the audio to MP3 and embeds the tags and artwork.

The result plays correctly in any music player.

## Features

- **Dashboard** — today's top tracks straight from Spotify charts, plus search by song or artist name (no URLs).
- **Download queue** — add tracks from the dashboard, review them on the Downloads page, and start the whole batch with one click.
- **Live status** — every job reports `pending` → `processing` → `done` (or `failed`), polled every 1–2 seconds.
- **Embedded metadata** — title, artist, album, track number, release date, and cover art.
- **Automatic download** — finished files are streamed to your browser as soon as every job in the batch completes.
- **Bulk queueing through the API** (`POST /job/bulk`).
- **Resilient workers** — up to 3 retry attempts per song before a job is marked failed.
- **Self-cleaning storage** — a background delete worker removes downloaded, failed, and abandoned files after `expires_in` seconds.

## Quickstart (Docker Compose)

**1. Configure the backend** (values from `.env.example` mostly work as-is):

```sh
cp backend/.env.example backend/.env.local
```

**2. Configure the frontend** (create `frontend/.env.local` if you don't have one):

```sh
echo "VITE_API_URL=http://localhost:8080" > frontend/.env.local
```

**3. Start everything**:

```sh
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend (nginx) | http://localhost:5173 |
| Backend API | http://localhost:8080 |

> **Note:** `VITE_API_URL` is baked into the JS bundle when the frontend image is built (`frontend/.env.local` is copied into the build). It runs in your **browser**, so use an address your browser can reach — `localhost` works when Docker is on the same machine, otherwise use the host's LAN IP — and re-run `docker compose up --build` after changing it.

## Manual setup

### Requirements

- Python 3.13+ and [uv](https://github.com/astral-sh/uv)
- Node.js 20+
- [ffmpeg](https://ffmpeg.org/) installed and on your `PATH`

No Spotify API credentials are needed — metadata comes from the scraper.

### 1. Backend

```sh
cd backend
uv sync --frozen
cp .env.example .env.local   # skip if you already have one; then edit as needed
uv run python src/main.py
```

The API starts on `http://127.0.0.1:8080`. **Run it from `backend/`** — config and temp paths are resolved relative to the working directory.

### 2. Frontend

```sh
cd frontend
npm install
echo "VITE_API_URL=http://127.0.0.1:8080" > .env.local   # skip if you already have one
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

## Configuration

All backend settings live in `backend/.env.local` (see `backend/.env.example`):

| Variable | Default | Purpose |
|---|---|---|
| `port` | `8080` | API port |
| `host` | `0.0.0.0` | API bind address |
| `env` | `development` | `development` enables uvicorn auto-reload (`.env.example` sets `production`) |
| `expires_in` | `3600` | Seconds before the delete worker removes a file (`.env.example` sets `60`) |
| `max_que` | `100` | Job queue capacity |
| `max_threads` | `3` | Number of worker threads |
| `allowed_origins` | `*` | CORS origins |
| `allowed_methods` | `GET,POST` | CORS methods |
| `spotify_client_id` / `spotify_client_secret` | — | Legacy — the current pipeline doesn't use them |
| `spotify_token_api` / `spotify_api` | Spotify endpoints | Legacy — kept for the unused token helper |

Frontend (in `frontend/.env.local`):

| Variable | Purpose |
|---|---|
| `VITE_API_URL` | Base URL of the backend, baked in at build time |

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python 3.13, FastAPI, Pydantic, yt-dlp, ffmpeg-python, spotify-scraper, uvicorn |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, react-router, Axios, react-hot-toast |
| Media | ffmpeg, Spotify charts/search (scraper) |
| Tooling | uv, npm, Docker Compose, pytest |

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/job` | Queue one song — `{"song": "..."}` → `201`; `503` if the queue stays full for 5s |
| `POST` | `/job/bulk` | Queue many songs at once — `[{"song": "..."}, ...]` |
| `GET` | `/status/{job_id}` | Live job status (`pending` / `processing` / `done` / `failed`); `404` if unknown |
| `GET` | `/download/{job_id}` | Stream the finished MP3 and mark the job as downloaded |
| `GET` | `/health` | Worker liveness (`active_workers`, `workers_health`) |
| `GET` | `/music` | Dashboard data — today's top hits chart |
| `GET` | `/music/search?q=<query>&limit=10` | Search tracks and artists |
| `GET` | `/music/data/{id}?type=track\|artist` | Full details for a track or artist |

## How it works

1. The browser sends a song request to the FastAPI backend (`POST /job`).
2. The job gets a UUID, is registered in the thread-safe job store, and is placed on an in-process queue (`queue.Queue`, capacity `max_que`).
3. Worker threads (count from `max_threads`, default 3) pull jobs off the queue and process them independently:
   - resolve the track through the Spotify scraper (canonical `Artist - Title` query),
   - download audio with yt-dlp,
   - fetch the cover art,
   - run ffmpeg to embed tags and artwork,
   - save the finished MP3 as `finished/<Artist - Title>_<job_id>.mp3`.
4. Retries: each job gets up to 3 attempts before being marked `failed`.
5. The frontend polls `/status/{job_id}` and triggers `/download/{job_id}` when the batch is done.
6. A **delete worker** sweeps every 30 seconds and removes downloaded files, failed jobs, and finished-but-never-downloaded files once they exceed `expires_in`.

The server and workers run in the same process and share a lock-guarded job store (`backend/src/core/state.py`), so status updates are immediately visible to the API. For a deeper design breakdown, see the local `architecture.md` design notes.

## Project structure

```
backend/
  src/
    main.py        # FastAPI app, CORS, /health, starts threads in lifespan
    worker.py      # worker + delete threads, download/tag pipeline
    routes/        # process.py (jobs), music.py (dashboard/search)
    core/          # config, file paths, thread-safe job & client stores
    models/        # Pydantic schemas and JOB_STATUS enum
    services/      # yt-dlp, Spotify scraper, ffmpeg, file helpers
    utils/         # timestamps and expiry helpers
    tests/         # pytest suite
    temp/          # jobs/ and finished/ (gitignored)
frontend/
  src/
    features/      # Dashboard, Download pages
    components/    # Navbar, Modal, Footer, Loading
    hooks/         # download queue + theme state
    services/      # Axios clients per endpoint group
docker-compose.yaml
architecture.md    # design/refactor document (dev notes)
```

## Development

```sh
# backend (from backend/)
uv run python src/main.py     # dev server
uv run pytest                 # tests

# frontend (from frontend/)
npm run dev                    # Vite dev server
npm run lint                   # ESLint
npm run build                  # tsc -b && vite build
```

## Known limitations

- **In-memory queue** — jobs are stored in process memory and are lost on restart.
- **Unofficial scraper** — metadata/search depend on `spotify-scraper`, which can break when Spotify changes its pages, and does its own rate limiting.
- **`VITE_API_URL` is baked in at build** — the frontend reads the API URL once when the bundle is built, so changing it means rebuilding (`docker compose up --build` or restarting Vite), and the value must be reachable from your browser.
- **No auth, wide-open CORS** (`allowed_origins=*`) — built for local/home-network use, not public hosting.
- **Files expire** — downloaded MP3s are deleted `expires_in` seconds after download; grab them before then.
- **Single node** — one process, one queue; no persistence or horizontal scaling.

## Status

🚧 **Work in progress** — features and structure may change.

## Disclaimer

This project is for educational and personal use. Downloading music may violate the terms of service of the source platforms and copyright law in your jurisdiction. Use responsibly.
