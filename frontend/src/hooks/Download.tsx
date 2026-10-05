import { downloadData } from "@/lib/lib";
import { checkStatus, createJob } from "@/services/process.service";
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

const formatSong = (job: Job) => { return `${job.name} ${job.artist}` }

export function DownloadProvider({ children }: { children: ReactNode }) {

  const [jobs, setJobs] = useState<Job[]>([]);


  const startDownload = async () => {
    let created: Job[] = [];
    for (const job of jobs) {
      const res = await createJob(formatSong(job));
      const updated = { ...job, job_id: res.job_id }
      created.push(updated);

      setJobs((prev) => prev.map((j) =>
        j.song_id === job.song_id ? { ...j, job_id: res.job_id } : j
      ));
    }

    while (true) {

      let checked = 0
      for (const job of created) {
        if (job.status === "done") continue;
        if (job.status === "failed") continue;

        const res = await checkStatus(job.job_id);
        job.status = res.status;
        setJobs((prev) => prev.map((j) =>
          j.job_id === job.job_id? { ...j, status: res.status } : j
        ));

        checked += 1;
      }

      if (checked ===0 ) break

      await new Promise((r) => setTimeout(r, 1000));
    }

    for (const job of created) { downloadData(job.job_id) }

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
