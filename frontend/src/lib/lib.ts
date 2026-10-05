import instance from "@/services/api.service";
import { getTrackData } from "@/services/music.service";
import { checkStatus, createJob } from "@/services/process.service";
import { toast } from "react-hot-toast";

export const downloadData = async (job_id: string) => {
   if (job_id === "") return;
   const res = await instance.get(`/download/${job_id}`, {
     responseType: "blob",
   });

   // Extract filename from Content-Disposition
   const disposition = res.headers["content-disposition"];
   const match = disposition?.match(/filename\*?=(?:UTF-8'')?["']?([^"';]+)/i);
   const filename = match ? decodeURIComponent(match[1]) : `track-${job_id}.mp3`;

   // Create a blob URL and trigger download
   const url = URL.createObjectURL(res.data);
   const a = document.createElement("a");
   a.href = url;
   a.download = filename;
   document.body.appendChild(a);
   a.click();
   a.remove();
   URL.revokeObjectURL(url);
 };


export const downloadNow = async (song_id: string) => {

  toast.promise(async () => {

    const data = await getTrackData(song_id);
    const job = await createJob(`${data.name} ${data.artists[0].name}`)
    while (true) {
      const res = await checkStatus(job.job_id);
      if (res.status === "done") break;

      await new Promise((r) => setTimeout(r, 2000));

    }
    downloadData(job.job_id);

  }, {
    loading: "Starting download...",
    error: "Failed to download",
    success: "Song has been downloaded!"
  });

}
