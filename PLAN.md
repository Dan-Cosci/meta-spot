# PLAN.md — Frontend restructure + browse/dashboard API contract

Plan for restructuring the meta-spot frontend around a router-backed SPA (Home / Browse / Dashboard), with the backend API contract the frontend needs.

---

## 0. Current state (what the plan starts from)

| Fact | Implication |
|---|---|
| `react-router-dom@7.18.3` installed, **never used** | No changes to package.json needed |
| `src/features/Dashboard.jsx`, `Download.jsx` — empty stubs, `.jsx` | eslint only lints `**/*.{ts,tsx}` and tsconfig has no `allowJs` → these files are invisible to lint **and** typecheck. Convert to `.tsx` or delete |
| Queue state + polling lives inside `App.tsx` | Navigating away would destroy it → lift into a context **above** the router |
| `Navbar` "home/about" are `<p>` tags | Replace with `NavLink`s |
| `handleDownload` does `api.get()` + `console.log(headers)` | **Broken** — axios buffers the file in memory, never saved. Fix as part of this work |
| nginx already has `try_files ... /index.html` | Client-side routes work in Docker with zero config changes |
| Backend: only `/job`, `/job/bulk`, `/status/{id}`, `/download/{id}`, `/health` | Browse + dashboard need the new endpoints in §4 |

---

## 1. Recommended folder structure

Feature-based (each feature owns its page, components, and API slice), with a thin shared layer. Sized for this app — don't over-nest.

```
frontend/src/
├── main.tsx                      # RouterProvider wraps the app + Toaster
├── app/
│   ├── router.tsx                # route table (single source of truth)
│   └── Layout.tsx                # Navbar + <Outlet /> + Footer shell
├── pages/
│   ├── HomePage.tsx              # current App.tsx content (queue + form)
│   ├── BrowsePage.tsx            # NEW — Spotify top-of-year + queue buttons
│   ├── DashboardPage.tsx         # NEW — most-downloaded charts
│   └── NotFoundPage.tsx          # catch-all
├── features/
│   └── queue/
│       ├── QueueContext.tsx      # queue state + polling, lives above router
│       ├── QueueList.tsx         # extracted from App.tsx lines 91–143
│       └── SearchForm.tsx        # extracted from App.tsx lines 75–89
├── components/
│   ├── Navbar.tsx                # real NavLinks
│   └── Footer.tsx
├── services/
│   ├── api.service.ts            # existing axios instance (keep)
│   ├── job.api.ts                # /job, /job/bulk, /status, /download
│   ├── browse.api.ts             # GET /browse/top
│   └── stats.api.ts              # GET /stats/top-downloads, /stats/summary
├── types/
│   ├── job.ts                    # Que, JobStatus
│   ├── track.ts                  # SpotifyTrack + download_count
│   └── stats.ts                  # LeaderboardEntry, Summary
├── config/config.ts              # existing
└── index.css
```

**Decisions baked in:**
- **Delete** `features/Download.jsx` — downloading is a button/action (`<a href>`), not a page. Keep a `Library` page as a future option if you later want "my downloads".
- **Rename** `Dashboard.jsx` stub → `pages/DashboardPage.tsx` (`.tsx`).
- `pages/` for routes, `features/` only for things with their own state/logic (queue). This keeps the tree shallow.

---

## 2. Router setup

Use `createBrowserRouter` (React Router v7's idiomatic data-router) with lazy routes so the dashboard/chart code doesn't bloat the home bundle:

```tsx
// src/app/router.tsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <NotFoundPage />,
    children: [
      { index: true, lazy: () => import("../pages/HomePage") },
      { path: "browse", lazy: () => import("../pages/BrowsePage") },
      { path: "dashboard", lazy: () => import("../pages/DashboardPage") },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
```

```tsx
// src/main.tsx
<StrictMode>
  <RouterProvider router={router} />
  <Toaster position="top-center" />
</StrictMode>
```

`Layout.tsx` = the shell currently in `App.tsx` (lines 70–72 + 148–149): outer div → `<Navbar />` → `<Outlet />` → `<Footer />`. The `QueueProvider` wraps the `RouterProvider` so queue state and its 2s polling survive navigation.

**Navbar** becomes:

```tsx
<NavLink to="/" end>Home</NavLink>
<NavLink to="/browse">Browse</NavLink>
<NavLink to="/dashboard">Dashboard</NavLink>
```

(drop the dead "about" link, or add an `/about` route — one or the other).

---

## 3. State strategy (the part that's easy to get wrong)

```
<QueueProvider>          ← owns que[], polling interval, submit/download handlers
  <RouterProvider />     ← pages consume useQueue()
    <Layout />           ← Navbar/Outlet/Footer
```

- **Queue state moves out of `HomePage`** into `QueueContext` — otherwise going to `/browse` and queueing a track, then navigating back, shows an empty queue.
- **Fix the polling while you're in there**: today's `useEffect` depends on `[que]`, so every status update tears down and recreates the interval. Use a `ref` holding the latest queue inside one stable interval (or poll only when there are non-terminal items).
- Browse page adds songs through the **same context** (`useQueue().add(query)`), so both pages feed one queue.
- No Redux/Zustand — context is correct at this scale.

---

## 4. API contract (backend endpoints the frontend will consume)

### New endpoints

**`GET /browse/top?year=2026&limit=50`** — Spotify proxy enriched with your stats

```json
{
  "success": true,
  "data": [
    {
      "spotify_id": "3n3Ppam7vgaVa1iaRUc9Lp",
      "title": "Mr. Brightside",
      "artist": "The Killers",
      "album": "Hot Fuss",
      "cover_url": "https://i.scdn.co/image/...",
      "popularity": 82,
      "download_count": 14
    }
  ]
}
```
- Implementation note: Spotify has no literal "top songs of 2026" endpoint — use `GET /v1/search?q=year:2026&type=track&limit=50`, then **sort by the `popularity` field descending server-side** (or proxy a known Top-50 playlist). Document whichever you pick in the README.
- `download_count` comes from your DB, `LEFT JOIN`ed on `spotify_id` (missing → `0`).

**`GET /stats/top-downloads?limit=20&period=all|week|month`**

```json
{
  "success": true,
  "data": [
    { "spotify_id": "...", "title": "...", "artist": "...", "cover_url": "...", "download_count": 42 }
  ]
}
```

**`GET /stats/summary`** (cheap to add, powers stat cards on the dashboard)

```json
{ "success": true, "data": { "total_downloads": 512, "total_tracks": 130, "total_queued": 140 } }
```

**`POST /job` — small additive change**: accept optional `"spotify_id"` alongside `"song"` so jobs queued **from Browse** attribute downloads to the right Spotify track. Free-text home-page queueing leaves it `null`.

### DB schema (SQLite, stdlib `sqlite3` — fits your zero-ORM setup)

```sql
CREATE TABLE IF NOT EXISTS tracks (
  spotify_id        TEXT PRIMARY KEY,          -- from Spotify track.id
  title             TEXT NOT NULL,
  artist            TEXT NOT NULL,
  album             TEXT,
  cover_url         TEXT,
  download_count    INTEGER NOT NULL DEFAULT 0,
  last_downloaded_at
);
```

**Instrumentation points** (two writes, nothing else):
1. **Worker on `DONE`** (`worker.py` after `tag_with_cover`): upsert title/artist/album/cover/`spotify_id` from the Spotify payload you already have.
2. **`/download/{job_id}` on success**: `download_count += 1`. (Counting here means "downloads" = actual file served — matches the "number of downloads" requirement.)

### Frontend service layer mirrors this 1:1

```ts
// services/browse.api.ts
export const getTopTracks = (year: number, limit = 50) =>
  api.get("/browse/top", { params: { year, limit } });

// services/stats.api.ts
export const getTopDownloads = (limit = 20, period = "all") =>
  api.get("/stats/top-downloads", { params: { limit, period } });
```

Typed with `types/track.ts` / `types/stats.ts` — one TS interface per response `data` shape above.

---

## 5. Page breakdown

| Route | Page | Contents |
|---|---|---|
| `/` | `HomePage` | Hero + `SearchForm` + `QueueList` (current UI, extracted not rewritten) |
| `/browse` | `BrowsePage` | Year selector (defaults to current year) → grid/table of `/browse/top` results; each row: cover, title, artist, `download_count` badge, **"Add to queue"** button → `useQueue().add()` |
| `/dashboard` | `DashboardPage` | Stat cards (`/stats/summary`) + ranked top-N table (`/stats/top-downloads`) styled Spotify-charts-like (rank, cover, title, artist, count) + period filter |
| `*` | `NotFoundPage` | Simple 404 + link home |

**On charts:** start with the ranked **table** — it *is* the Spotify-charts look, needs no new dependency, and matches the "download counts only" decision. Add `recharts` later only if you want time-series graphs (that would require a daily snapshot table — future work, not v1).

**Cover art:** the Browse page can show Spotify `cover_url` directly (CDN hotlinking is normal for this). For Dashboard rows you can do the same — don't proxy images through your backend.

---

## 6. Implementation order

1. **Fix `handleDownload` first** — it's broken now; download via a real anchor: `<a href={`${api_url}/download/${id}`} download>` (backend already sends `Content-Disposition: attachment`). Don't route downloads.
2. **Router skeleton**: `app/router.tsx` + `app/Layout.tsx` + `main.tsx` swap; move current `App.tsx` body → `pages/HomePage.tsx`; Navbar → `NavLink`s. Verify all routes render.
3. **Extract `QueueContext`** (state + polling + submit/download handlers); wire `HomePage` to it.
4. **Types + service layer**: `types/*.ts`, `job.api.ts` / `browse.api.ts` / `stats.api.ts`.
5. **Backend contract** (endpoints + SQLite + 2 instrumentation writes) — frontend pages can be built against the JSON shapes above with mocked services if you want to parallelize.
6. **`BrowsePage`**, then **`DashboardPage`**.
7. **Cleanup**: delete `features/Download.jsx`, rename stub → `.tsx`, `npm run lint && npm run build`, then **enable `strict: true`** in `tsconfig.app.json` while the surface is fresh (REVIEW_2 #14).

---

## 7. Watch-outs

- **`.jsx` stubs are a trap** — they pass through lint/typecheck untouched. Everything new in `.tsx`.
- **Don't put `QueueProvider` inside a route** — it must sit above `RouterProvider` or the queue resets on every navigation.
- **`/browse/top` needs the year parameter validated** (reject weird values) and a short cache (e.g. 5 min in-memory) — Spotify rate-limits are real, and a dashboard polling spamming search will get you 429s.
- **README/API table** must gain the three new endpoints when you build them (it already drifts once — see REVIEW_2).
- The queue's 404-removal logic (`App.tsx:35-40`) moves to `QueueContext` unchanged — it's correct now.