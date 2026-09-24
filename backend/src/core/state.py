
import threading

from spotify_scraper import SpotifyClient

from models import JOB_QUE, JOB_RESPONSE, JOB_STATUS
from utils import get_current_timestamp


class _job_store:
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
                created_at=get_current_timestamp()
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

    def list_done(self) -> list:
        with self.lock:
            return [key for key, i in self.jobs.items() if i.status == JOB_STATUS.DONE and not i.is_downloaded]


class _client_store:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.clients: dict[int, SpotifyClient] = {}

    def register(self, worker_id: int, proxy: str | None = None):
        client = SpotifyClient(proxy=proxy, timeout=15)
        with self.lock:
            self.clients[worker_id] = client
        return client

    def get(self, worker_id) -> SpotifyClient:
        with self.lock:
            try:
                return self.clients[worker_id]

            except KeyError:
                raise RuntimeError(f"error client_store: {worker_id} does not have clients assigned to them")

    def close_all(self):
        with self.lock:
            for client in self.clients.values():
                client.close()

            self.clients.clear()






job_store = _job_store()
client_store = _client_store()
