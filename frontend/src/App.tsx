import { useEffect, useState, type SubmitEvent } from "react";
import Logo from "./assets/meta-spot-logo.svg"
import toast from "react-hot-toast";
import api from "./services/api.service";
import Footer from "./components/Footer";

interface Que {
  query: string;
  status: string;
  job_id: string;
}

export default function App() {
  const [query, setQuery] = useState<string>("");
  const [que, setQue] = useState<Que[]>();

  useEffect(() => {
    const interval = setInterval(async () => {
      // skips 1st run
      if (!que) return;

      for (const item of que) {
        if (item.status !== "done") {
          const res = await api.get(`/status/${item.job_id}`, {});
          setQue((prev) => (prev ?? []).map((q) =>
            q.job_id == item.job_id ? {...q, status: res.data.status[0]}:q
          ));
        }
      }

    }, 2000);

    return () => clearInterval(interval)
  }, [que]);

  const handleInsert = async (e: SubmitEvent) => {
    e.preventDefault();
    if (query === "") {
      toast.error("You can't submit blank");
      return;
    }

    const song = query;
    const res = await api.post("/job", { song: song });
    const data = res.data.data;
    setQue((prev) => [...(prev ?? []), { query: song, status: "pending", job_id:data.job_id}]);
    setQuery("");

    if (!que) return;
    for (const item of que) console.log(item);
  }

  const handleDownload = async (job_id: string) => {
    if (job_id === "") return;
    window.location.href = `${api.defaults.baseURL}/download/${job_id}`
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

      <main className="h-full flex-1 max-md:px-4 md:px-[10vw] flex flex-col items-center text-center max-md:pt-10 pt-18">
          <h1 className="text-3xl font-bold">Own your <span className="text-green-300">music</span>, Listen without the <span className="text-green-300">subscription</span></h1>
          <form onSubmit={handleInsert} className="flex max-md:flex-col p-8 md:items-center items-end">
            <input
              type="text"
              name="song"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Song name - artist name..."
              className="bg-neutral-900 border border-green-300 rounded-4xl focus:outline-none max-md:w-[80vw] w-[50vw] text-xl px-8 py-3 max-md:mb-4"
            />
            <button type="submit" className="bg-transparent w-32 h-10  max-md:ml-0 ml-5 rounded-4xl text-green-300 border-2 border-green-300 hover:bg-green-300 hover:text-white hover:scale-105 transition-all duration-150 active:scale-95">
              add to que
            </button>
          </form>

          {que && (
            <section className="w-full max-w-2xl flex flex-col gap-3">
              {/* Header */}
              <div className="flex flex-row justify-between items-center">
                <h2 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider">
                  Queue
                </h2>
                <span className="text-sm text-neutral-500">{que.length} songs</span>
              </div>

              {/* Items */}
              <div className="flex flex-col gap-2">
                {que.map((item, i) => (
                  <div
                    key={i}
                    className="flex flex-row items-center justify-between
                               px-4 py-3 rounded-lg border border-neutral-800
                               bg-neutral-800/50"
                  >
                    {/* Left: status icon */}
                    <div className="flex flex-row items-center gap-3">
                      {item.status === "done" && <span className="text-green-400">✓</span>}
                      {item.status === "pending" && <span className="text-amber-300 animate-pulse">·</span>}
                      {item.status === "failed" && <span className="text-red-400">✕</span>}

                      <span className="truncate max-w-[40ch]">{item.query}</span>
                    </div>

                    {/* Right: status label */}
                    <span
                      className={`text-xs shrink-0 ml-3 ${
                        item.status === "done" ? "text-green-400"
                        : item.status === "pending" ? "text-amber-300"
                        : item.status === "failed" ? "text-red-400"
                        : "text-neutral-500"
                      }`}
                    >
                      {item.status === "pending" &&
                        <div className="h-3 w-3 animate-spin rounded-full border-2 border-amber-300 border-t-transparent inline-block mr-2"></div>
                      }
                      {item.status}
                      {item.status === "done" &&
                        <button className="ml-4 bg-green-300 text-white font-semibold px-2 py-1 rounded-4xl transition-all duration-150 active:scale-95"
                          onClick={ () => handleDownload(item.job_id) }>
                          Download
                        </button>
                      }
                    </span>
                  </div>
                ))}
              </div>
            </section>
          )}

      </main>


      </div>
      <Footer />

    </>
  );
}
