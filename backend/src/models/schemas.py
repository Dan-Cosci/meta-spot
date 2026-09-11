
from pydantic import BaseModel
from uuid import UUID


class job_req(BaseModel):
    song: str

class job_return(job_req):
    job_id: UUID
