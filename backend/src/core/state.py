
import threading

from models import JOB_QUE, JOB_RESPONSE, JOB_STATUS


class job_store:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.jobs = {}

    def init_job(self, job: JOB_RESPONSE):
        with self.lock:
            self.jobs[str(job.job_id)] = JOB_QUE(
                status=JOB_STATUS.PENDING,
                file_name=None,
                file_path=None,
                job_id=job.job_id,
                song=job.song
            )

    def update_status(self, job_id, status: JOB_STATUS):
        with self.lock:
            key = str(job_id)
            if key in self.jobs:
                self.jobs[key].status = status

    def update_job(self, job_id, item: JOB_QUE):
        with self.lock:
            key = str(job_id)
            if key in self.jobs:
                self.jobs[key] = item

    def get(self, job_id):
        with self.lock:
            return self.jobs.get(str(job_id), None)

store = job_store()
