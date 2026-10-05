import { useEffect, useRef, useState } from "react";
import Modal from "@/components/Modal";
import type { TrackData } from "@/types";
import { getTopTracks, getTrackData } from "@/services/music.service";
import Loading from "@/components/Loading";
import { downloadNow } from "@/lib/lib";
import { useDownload } from "@/hooks/Download";

function Dashboard() {
  const [selected, setSelected] = useState<TrackData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [play, setPlay] = useState<boolean>(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);

  const [tracks, setTracks] = useState<TrackData[]>([]);
  const open = selected ? true : false;

  const { addSong, jobs } = useDownload();

  // fetch top songs
  useEffect(() => {
    console.log("this is ran once")

    const fetchtracks = async () => {
      setLoading(true)
      const data: TrackData[] = await getTopTracks()
      setTracks(data ?? []);
      console.log(data)
    }

    fetchtracks().then(() => setLoading(false));

  }, []);

  // player logic
  useEffect(() => {
    const a = audioRef.current;
    if (!a) return;

    const onTime = () => setCurrent(a.currentTime);
    const onMeta = () => setDuration(a.duration);
    const onPlay = () => setPlay(true);
    const onPause = () => setPlay(false);
    const onEnded = () => {
      setPlay(false);
      setCurrent(0);
    };

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
    setPlay(prev => !prev);
    if (!a) return;
    a.paused ? a.play().catch(() => { }) : a.pause();
  }



  const handleClick = async (el: TrackData) => {
    const a = audioRef.current;
    if (!a) return;

    a.pause();
    setCurrent(0);
    setDuration(0);
    setPlay(false);

    const data: TrackData = await getTrackData(el.id);
    setSelected(data)


    if (!data.preview_url) return;
    a.src = data.preview_url;
    a.load();
  }

  return (
    <>
      <audio ref={audioRef} />
      <div className="p-4 flex gap-4">
        <input
          className="px-5 py-2 border-main border-2 outline-0 rounded-full w-[80vw] md:w-[50vw] "
          type="text"
        />
        <button
          className="btn-animation bg-main px-4 py-2 rounded-full"
          onClick={() => console.log(jobs)}
        >
          Search
        </button>
      </div>
      {loading ? <Loading /> :<>
      <section className="flex gap-1 overflow-scroll w-full scrollbar-none">
        {tracks.map(el => (
          <div className="bg-background shrink-0 w-2xs p-2 flex items-start rounded-2xl gap-4 hover:bg-card-hover">
            <div className="w-18 h-18 rounded-xl overflow-hidden shrink-0">
              <img src={el.images[2].url} alt="" className="h-full w-full" />
            </div>
            <div className="flex flex-col justify-center items-baseline">
              <h1 className="font-bold text-md">{el.name.length >= 21 ? `${el.name.slice(0,21).concat("...")}`: el.name}</h1>
              <p className="text-sm text-text-muted">{el.artists[0].name}</p>
            </div>
          </div>
        ))}
      </section>
      <section className="grid grid-cols-2 md:grid-cols-5 mt-8 gap-2">
        {tracks.map(el => (
          <div key={ el.id } className="rounded-xl p-2 hover:bg-card-hover" onClick={()=>handleClick(el)}>
            <img src={ el.images[0].url } alt="" className="rounded-xl"/>
            <div className="flex flex-col items-baseline">
              <h1 className="font-bold text-md">{el.name.length >= 22 ? `${el.name.slice(0,22).concat("...")}`: el.name}</h1>
              <p className="text-sm text-text-muted">{el.artists[0].name}</p>
            </div>
          </div>
        ))}
      </section>
      </>}
      {selected &&
        <Modal open={open} onClose={onClose}>
          <div className="mx-8 p-4 w-auto md:min-w-[40vw] h-auto bg-neutral-800 rounded-lg border-2 border-neutral-600 overflow-hidden flex flex-col gap-4">
            <div className="flex items-start justify-start">
              <div className=" w-20 h-20 shrink-0 rounded-lg overflow-hidden">
                <img src={selected.images[2].url} alt="" className="h-full md:w-auto" />
              </div>
              <div className="flex-1 flex flex-col items-baseline px-4">
                <h1 className="text-xl font-bold">{selected.name}</h1>
                <h2 className="text-md">{ selected.artists[0].name}</h2>
              </div>
            </div>
            <div className="flex gap-4">
              <button onClick={toggle}>{ play ? "pause" : "play"}</button>
              <p>{ current }</p>
              <input
                type="range"
                className="flex-1"
                value={current}
                min={0}
                max={duration|| 0}
                onChange={(e) => {
                  const a = audioRef.current;
                  if (!a) return;
                  const t = Number(e.target.value);
                  a.currentTime = t;
                  setCurrent(t);
                }}
              />
              <p>{ duration }</p>
            </div>
            <div className="flex justify-center items-center gap-4">
              <button className="bg-main p-2 rounded-md w-full btn-animation" onClick={() => downloadNow(selected.id)}>Download now</button>
              <button className="bg-main p-2 rounded-md w-full btn-animation" onClick={() => addSong(selected)}>Add to Downloads</button>
            </div>
          </div>
        </Modal>
      }
    </>
  );
}

export default Dashboard;
