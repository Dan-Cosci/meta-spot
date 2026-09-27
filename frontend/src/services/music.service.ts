import type { PlaylistResponse, TrackData, TrackResponse } from "@/types";
import instance from "./api.service";

const api = instance;

export const getTrackData = async (id: string): Promise<TrackData> => {
  const res = await api.get<TrackResponse>(`/music/data/${id}?type=track`);
  return res.data?.data
}

export const getTopTracks = async (): Promise<TrackData[] | []> => {
  const res = await api.get<PlaylistResponse>("/music");
  const tracks = (res.data.data?.tracks ?? []).map((i)=> i.track);
  return tracks;

}
