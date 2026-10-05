import instance from "./api.service";

export const createJob = async (song_name: string) => {
  const res = await instance.post("/job", { song: song_name });
  return res.data.data;
}

export const checkStatus = async (job_id: string) => {
  const res = await instance.get(`/status/${job_id}`);
  return res.data.data;
}
