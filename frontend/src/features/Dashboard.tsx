import { useEffect, useState } from "react";
import { tracks } from "../fake-data"
import Modal from "@/components/Modal";

function Dashboard() {
  const [selected, setSelected] = useState<any>(null);
  const open = selected ? true : false;

  const onClose = () => {
    setSelected(null);
  }

  useEffect(() => {
    console.log("this is ran once")
  });



  return (
    <>
      {/* popular */}
      <section className="flex gap-5 overflow-scroll w-full scrollbar-none">
        {tracks.map(el => (
          <div className="bg-neutral-800 shrink-0 w-[16rem] flex rounded-2xl gap-4">
            <img src={ el.track.images[0].url } alt="" className="w-18 h-18 rounded-2xl"/>
            <div className="flex flex-col justify-center items-baseline">
              <h1 className="">{el.track.name}</h1>
              <p className="text-sm text-green-800">{el.track.artists[0].name}</p>
            </div>
          </div>
        ))}
      </section>
      <section className="grid grid-cols-2 md:grid-cols-4 mt-16 gap-3.5">
        {tracks.map(el => (
          <div key={ el.track.id } className="rounded-xl p-2 hover:bg-green-900" onClick={()=> setSelected(el)}>
            <img src={ el.track.images[0].url } alt="" className="rounded-xl"/>
            <div className="">
              <h1 className="">{el.track.name}</h1>
              <p className="">{el.track.artists[0].name}</p>
            </div>
          </div>
        ))}
      </section>
      {selected &&
        <Modal open={open} onClose={onClose}>
          <div className="w-screen h-[75vh] md:w-[80vw] md:h-[80vh] bg-neutral-800/90 rounded-3xl border-2 border-neutral-600">
            <img src={ selected.track.images[2].url } alt="" />
            {selected.track.name}
            {selected.track.artists[0].name}
            {selected.release_date}
          </div>
        </Modal>
      }
    </>
  );
}

export default Dashboard;
