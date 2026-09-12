import { useEffect, useState, SubmitEvent } from "react";
import Logo from "./assets/meta-spot-logo.svg"

interface Que {
  query: string;
  status: string;

}

export default function App() {
  const [query, setQuery] = useState<string>("");
  const [que, setQue] = useState<Que[]>();


  useEffect(() => {

  }, [que]);

  const handleInsert = (e: SubmitEvent) => {
    e.preventDefault();
    const song = query;
    setQue((prev) => [...(prev ?? []), { query: song, status: "pending" }]);
    setQuery("");

  }

  return (
    <>
      <div className="min-h-screen min-w-screen bg-neutral-900 text-white flex flex-col">
      <nav className="max-md:px-4 md:px-[10vw] py-4 flex flex-row justify-between items-center">
        <div className="flex flex-row justify-between items-center gap-3">
          <img src={Logo} alt="meta spot logo" className="max-md:w-12  md:w-14" />
          <h2 className="font-bold max-md:text-2xl md: text-2xl">Meta-spot</h2>
        </div>
        <div className="flex flex-row justify-between items-center gap-5">
          <p className="text-lg hover:text-green-300">home</p>
          <p className="text-lg hover:text-green-300">about</p>
        </div>
      </nav>

      <main className="h-full flex-1 max-md:px-4 md:px-[10vw] flex flex-col items-center justify-center">
          <h1>Make your mp3 complete with album covers and meta data</h1>
          <form onSubmit={handleInsert}>
            <input
              type="text"
              name="song"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Song name - artist name..."
          />
            <button type="submit" className="bg-amber-200">
              add to que</button>
          </form>

          {que &&
            <div className="h-10 border-2 border-green-800 rounded-md p-2">
              { que.map((e) => (e.query))}
            </div>
          }

      </main>


      </div>
      <footer>
        <h2>Meta-spot</h2>
      </footer>
    </>
  );
}
