
from enum import Enum

from pydantic import BaseModel
from uuid import UUID

class JOB_STATUS(Enum):
    pending = 0,
    processing = 1,
    done = 3


class JOB_REQUEST(BaseModel):
    song: str

class JOB_RESPONSE(JOB_REQUEST):
    job_id: UUID

class JOB_QUE(JOB_RESPONSE):
    status: JOB_STATUS
    file_name: str | None = None
    is_downloaded: bool = False
    finished_at: float | None = None
