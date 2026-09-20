
import threading
from datetime import datetime

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
                song=job.song,
                created_at=datetime.now().timestamp()
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

    def get(self, job_id) -> JOB_QUE | None:
        with self.lock:
            return self.jobs.get(str(job_id), None)

    def delete(self, job_id):
        with self.lock:
            return self.jobs.pop(job_id)

    def list_downloaded(self) -> list:
        with self.lock:
            return [key for key,i in self.jobs.items() if i.is_downloaded]

    def list_failed(self) -> list:
        with self.lock:
            return [key for key, i in self.jobs.items() if i.status == JOB_STATUS.FAILED]

store = job_store()
