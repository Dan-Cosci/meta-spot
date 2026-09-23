export type QueStatus = "pending" | "failed" | "done" | "processing"
export interface Que {
  query: string;
  status: QueStatus;
  job_id: string;
}
