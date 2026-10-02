import { useEffect, useRef, useState } from "react";
import Modal from "@/components/Modal";
import type { TrackData } from "@/types";
import { getTopTracks, getTrackData } from "@/services/music.service";
import Loading from "@/components/Loading";

function Dashboard() {
  const [selected, setSelected] = useState<TrackData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [play, setPlay] = useState<boolean>(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);

  const [tracks, setTracks] = useState<TrackData[]>([]);
  const open = selected ? true : false;

  const onClose = () => {
    setSelected(null);
    audioRef.current?.pause()
  }

  const toggle = () => {
    const a = audioRef.current;
    setPlay(prev => !prev);
    if (!a) return;
    a.paused ? a.play().catch(() => { }) : a.pause();
  }

  useEffect(() => {
    console.log("this is ran once")

    const fetchtracks = async () => {
      setLoading(true)
      const data: TrackData[] = await getTopTracks()
      setTracks(data ?? []);
      console.log(data)
    }

    fetchtracks().then(() => setLoading(false));

  },[]);


  const handleClick = async (el: TrackData) => {
    const data: TrackData = await getTrackData(el.id);
    console.log(data)
    setSelected(data)



    audioRef.current.src = data.preview_url;
    audioRef.current.currentTime = 0;

    console.log(Number(audioRef.current?.duration))
  }

  return (
    <>
      <audio ref={audioRef} />
      {loading ? <Loading /> :<>
      <section className="flex gap-5 overflow-scroll w-full scrollbar-none">
        {tracks.map(el => (
          <div className="bg-background shrink-0 w-[16rem] flex rounded-2xl gap-4">
            <div className="w-18 h-18 rounded-2xl overflow-hidden">
              <img src={el.images[2].url} alt="" className="h-full w-full" />
            </div>
            <div className="flex flex-col justify-center items-baseline">
              <h1 className="">{el.name}</h1>
              <p className="text-sm text-green-800">{el.artists[0].name}</p>
            </div>
          </div>
        ))}
      </section>
      <section className="grid grid-cols-2 md:grid-cols-4 mt-16 gap-3.5">
        {tracks.map(el => (
          <div key={ el.id } className="rounded-xl p-2 hover:bg-green-900" onClick={()=>handleClick(el)}>
            <img src={ el.images[0].url } alt="" className="rounded-xl"/>
            <div className="">
              <h1 className="">{el.name}</h1>
              <p className="">{el.artists[0].name}</p>
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
              <p>0:00</p>
              <input type="range" className="flex-1" />
              <p>3:14</p>
            </div>
            <div className="flex justify-center items-center gap-4">
              <button className="bg-green-800 p-2 rounded-md w-full">Download now</button>
              <button className="bg-green-800 p-2 rounded-md w-full">Add to Downloads</button>
            </div>
          </div>
        </Modal>
      }
    </>
  );
}

export default Dashboard;
