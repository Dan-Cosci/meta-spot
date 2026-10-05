import type { jobModel, jobStatusModel, TrackData } from "@/types"
import { createContext, useContext, useState, type ReactNode } from "react";
type Job = {
  job_id: string | null
  song_id: string
  name: string
  artist: string
  status: "done" | "pending" | "processing" | "failed"
}

type DownloadContextValue = {
  jobs: Job[]
  startDownload: () => void
  addJob: (job: jobModel) => void
  addSong: (song: TrackData) => void
}

const downloadContext = createContext<DownloadContextValue>(null)

export function DownloadProvider({ children }: { children: ReactNode }) {

  const [jobs, setJobs] = useState<Job[]>([]);
  const startDownload = () => {
    for (const job of jobs) {
      console.log(job);
    }
  }

  const addJob = (job: jobModel) => { }
  const addSong = (song: TrackData) => setJobs((prev) => ([...prev ?? [], {
   job_id: null, song_id: song.id, name: song.name, artist: song.artists[0].name, status: "pending"
  }]));
  const updateStatus = (job: jobStatusModel) => { }


  return (
    <downloadContext.Provider value={{startDownload, jobs, addJob, addSong}}>
      { children }
    </downloadContext.Provider>
  )
}


export function useDownload() {
  const ctx = useContext(downloadContext);
  if (!ctx) throw new Error("Hook must be used under DownloadProvider");
  return ctx;
}
