import { useEffect, useRef, useState } from "react";
import Modal from "@/components/Modal";
import type { TrackData } from "@/types";
import { getTopTracks, getTrackData } from "@/services/music.service";
import Loading from "@/components/Loading";
import { useDownload } from "@/hooks/Download";

function formatTime(seconds: number) {
  if (!isFinite(seconds) || seconds <= 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function truncate(text: string, max = 22) {
  return text.length > max ? `${text.slice(0, max)}…` : text;
}

function Dashboard() {
  const [selected, setSelected] = useState<TrackData | null>(null);
  const [loading, setLoading] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [play, setPlay] = useState(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);

  const [tracks, setTracks] = useState<TrackData[]>([]);
  const open = selected !== null;

  const { addSong, jobs } = useDownload();

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const data = await getTopTracks();
        if (!cancelled) setTracks(data ?? []);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    const a = audioRef.current;
    if (!a) return;

    const onTime = () => setCurrent(a.currentTime);
    const onMeta = () => setDuration(a.duration);
    const onPlay = () => setPlay(true);
    const onPause = () => setPlay(false);
    const onEnded = () => { setPlay(false); setCurrent(0); };

    a.addEventListener("timeupdate", onTime);
    a.addEventListener("loadedmetadata", onMeta);
    a.addEventListener("play", onPlay);
    a.addEventListener("pause", onPause);
    a.addEventListener("ended", onEnded);

    return () => {
      a.removeEventListener("timeupdate", onTime);
      a.removeEventListener("loadedmetadata", onMeta);
      a.removeEventListener("play", onPlay);
      a.removeEventListener("pause", onPause);
      a.removeEventListener("ended", onEnded);
    };
  }, []);

  const onClose = () => {
    setSelected(null);
    setPlay(false);
    setCurrent(0);
    setDuration(0);
    audioRef.current?.pause();
  };

  const toggle = () => {
    const a = audioRef.current;
    if (!a || !a.src) return;
    if (a.paused) a.play().catch(() => {});
    else a.pause();
  };

  const seek = (t: number) => {
    const a = audioRef.current;
    if (!a) return;
    a.currentTime = t;
    setCurrent(t);
  };

  const handleClick = async (el: TrackData) => {
    const a = audioRef.current;
    a?.pause();
    setCurrent(0);
    setDuration(0);
    setPlay(false);

    const data = await getTrackData(el.id);
    setSelected(data);

    if (a && data.preview_url) {
      a.src = data.preview_url;
      a.load();
    }
  };

  const hasPreview = Boolean(selected?.preview_url);

  return (
    <>
      <audio ref={audioRef} />

      {/* Search */}
      <div className="flex w-full max-w-2xl gap-3">
        <input
          type="text"
          placeholder="Search tracks…"
          className="w-full rounded-full border-2 border-highlight bg-transparent px-5 py-2.5 text-text-main outline-none transition-colors placeholder:text-text-muted focus:border-main"
        />
        <button
          onClick={() => console.log(jobs)}
          className="btn-animation shrink-0 rounded-full bg-main px-6 py-2.5 text-sm font-medium text-background"
        >
          Search
        </button>
      </div>

      {loading ? (
        <Loading />
      ) : (
        <div className="w-full max-w-6xl text-left">
          {/* Popular — horizontal scroll */}
          <section className="mt-10">
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-widest text-text-muted">
              Popular now
            </h2>
            <div className="flex gap-3 overflow-x-auto pb-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
              {tracks.map((el) => (
                <button
                  key={el.id}
                  onClick={() => handleClick(el)}
                  className="flex w-72 shrink-0 items-center gap-4 rounded-2xl bg-highlight/20 p-3 text-left transition-colors hover:bg-card-hover"
                >
                  <div className="h-16 w-16 shrink-0 overflow-hidden rounded-xl">
                    <img src={el.images[2].url} alt="" className="h-full w-full object-cover" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-semibold">{truncate(el.name, 21)}</p>
                    <p className="truncate text-sm text-text-muted">{el.artists[0].name}</p>
                  </div>
                </button>
              ))}
            </div>
          </section>

          {/* Grid */}
          <section className="mt-10">
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-widest text-text-muted">
              All tracks
            </h2>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {tracks.map((el) => (
                <button
                  key={el.id}
                  onClick={() => handleClick(el)}
                  className="group rounded-xl p-2 text-left transition-colors hover:bg-card-hover"
                >
                  <div className="aspect-square w-full overflow-hidden rounded-xl">
                    <img
                      src={el.images[0].url}
                      alt=""
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                  </div>
                  <p className="mt-2 truncate font-semibold">{truncate(el.name)}</p>
                  <p className="truncate text-sm text-text-muted">{el.artists[0].name}</p>
                </button>
              ))}
            </div>
          </section>
        </div>
      )}

      {/* Player modal */}
      {selected && (
        <Modal open={open} onClose={onClose}>
          <div className="mx-4 flex w-[calc(100vw-2rem)] max-w-md flex-col gap-5 rounded-2xl border border-highlight bg-background p-5 shadow-xl md:mx-0 md:w-[28rem]">
            {/* Track header */}
            <div className="flex items-start gap-4">
              <div className="h-20 w-20 shrink-0 overflow-hidden rounded-xl">
                <img src={selected.images[2].url} alt="" className="h-full w-full object-cover" />
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="truncate text-xl font-bold">{selected.name}</h1>
                <p className="truncate text-text-muted">{selected.artists[0].name}</p>
              </div>
            </div>

            {/* Player */}
            {hasPreview ? (
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <button
                    onClick={toggle}
                    aria-label={play ? "Pause" : "Play"}
                    className="btn-animation flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-main text-background"
                  >
                    {play ? (
                      <svg viewBox="0 0 24 24" className="h-5 w-5 fill-current">
                        <rect x="6" y="5" width="4" height="14" rx="1" />
                        <rect x="14" y="5" width="4" height="14" rx="1" />
                      </svg>
                    ) : (
                      <svg viewBox="0 0 24 24" className="h-5 w-5 fill-current">
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    )}
                  </button>

                  <span className="w-10 text-right text-xs tabular-nums text-text-muted">
                    {formatTime(current)}
                  </span>

                  <input
                    type="range"
                    min={0}
                    max={duration || 0}
                    value={current}
                    onChange={(e) => seek(Number(e.target.value))}
                    className="h-1 w-full cursor-pointer appearance-none rounded-full bg-highlight accent-main"
                  />

                  <span className="w-10 text-xs tabular-nums text-text-muted">
                    {formatTime(duration)}
                  </span>
                </div>
                <p className="text-center text-xs text-text-muted">30-second preview</p>
              </div>
            ) : (
              <div className="rounded-xl border border-highlight/50 bg-highlight/20 p-4 text-center text-sm text-text-muted">
                No preview available for this track
              </div>
            )}

            {/* Actions */}
            <div className="flex flex-col gap-2 sm:flex-row">
              <button
                onClick={() => addSong(selected)}
                className="btn-animation flex-1 rounded-xl border border-highlight px-4 py-2.5 text-sm font-medium transition-colors hover:bg-card-hover"
              >
                Add to Downloads
              </button>
              <button
                onClick={() => addSong(selected)}
                className="btn-animation flex-1 rounded-xl bg-main px-4 py-2.5 text-sm font-medium text-background"
              >
                Download now
              </button>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}

export default Dashboard;
