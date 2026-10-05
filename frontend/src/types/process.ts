export type jobStatus = "done" | "pending" | "failed" | "processing"
export type jobModel = {
  job_id: string
  song: string
}
export type jobStatusModel = {
  job_id: string
  status: jobStatus
}

export type jobRes = {
  succes: boolean
  message: string
  data: jobModel | jobStatusModel | null
}
