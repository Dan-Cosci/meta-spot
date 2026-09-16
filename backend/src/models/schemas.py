
from enum import Enum
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel


class JOB_STATUS(Enum):
    PENDING = "pending",
    PROCESSING = "processing",
    DONE = "done",
    FAILED = "failed"


class JOB_REQUEST(BaseModel):
    song: str

class JOB_RESPONSE(JOB_REQUEST):
    job_id: UUID

class JOB_QUE(JOB_RESPONSE):
    status: JOB_STATUS
    file_name: str | None = None
    file_path: str | Path | None = None
    is_downloaded: bool = False
    finished_at: float | None = None
