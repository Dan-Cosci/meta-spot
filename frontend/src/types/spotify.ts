export interface TrackResponse {
  success: boolean;
  message: string;
  data: TrackData | null;
}

export interface SearchResponse {
  success: boolean;
  message: string;
  data: SearchData | null;
}

export interface PlaylistResponse {
  success: boolean;
  message: string;
  data: PlaylistData | null;
}

export interface TrackData {
  id: string;
  uri: string;
  name: string;
  duration_ms: number;
  preview_url: string | null;
  artists: Artist[];
  images: Image[];
  release_date: string | null;
  album: Album | null;
  play_count: number | null;
}

export interface ArtistData {
  id: string;
  uri: string;
  name: string;
  images: Image[];
  biography: string | null;
  followers: number;
  monthly_listeners: number | null;
  top_tracks: TrackData[];
}

export interface PlaylistTrack {
  track: TrackData;
  added_at: string | null;
  added_by: Artist | null;
}

export interface PlaylistData {
  id: string;
  name: string;
  description: string | null;
  followers: number | null;
  tracks: PlaylistTrack[];
}

export interface Artist {
  name: string;
  uri: string;
  id: string;
}

export interface Image {
  url: string;
  width: number | null;
  height: number | null;
}

export interface Album {
  id: string;
  uri: string;
  name: string;
  images: Image[];
}


export interface SearchData {
  query: string
  tracks: TrackData[]
  artists: ArtistData[]
}
