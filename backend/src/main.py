
from uuid import uuid4

from fastapi import FastAPI
from fastapi.routing import JSONResponse
from core import api
from models.schemas import job_req, job_return
from core.files import QUE_DIR
from services.file_service import write_file


app = FastAPI()

@app.post("/job")
async def create_job(req: job_req):
    id = uuid4()
    job = job_return(
        job_id=id,
        song=req.song
    )
    write_file(base=QUE_DIR, file_name=f"{id}", data=job.model_dump_json())
    return {
        "success": True,
        "Message": "Hello from fastapi",
        "data": job.model_dump()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api["port"],
        host=api["host"],
        reload=True,
        use_colors=True
    )
