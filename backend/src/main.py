
from contextlib import asynccontextmanager
from pathlib import Path
from queue import Queue
import threading
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from core import FINISHED_DIR, QUE_DIR, api_settings
from models import JOB_QUE, JOB_REQUEST, JOB_RESPONSE
from services import write_file
from worker import worker

PROCESS_QUE: Queue = Queue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("process start")

    stop = threading.Event()
    t = [
        threading.Thread(target=worker, args=(i, PROCESS_QUE, stop), name=f"worker: {i}")
        for i in range(3)
    ]

    for i in t:
        i.start()

    yield

    stop.set()
    for i in t:
        i.join(timeout=30)

    print("process ended")

app = FastAPI(lifespan=lifespan)

@app.get("/job/{job_id}")
async def get_job_details(job_id):
    return {
        "success": True,
        "Message": "Hello from fastapi",
        "data": job_id
    }

@app.post("/job")
async def create_job(req: JOB_REQUEST):
    id = uuid4()
    job = JOB_RESPONSE(
        job_id=id,
        song=req.song
    )
    PROCESS_QUE.put(job)
    return {
        "success": True,
        "Message": "Created request",
        "data": job.model_dump()
    }


@app.post("/job/bulk")
async def bulk_create_job(req: list[JOB_REQUEST]):

    jobs = []
    for i in req:
        id = uuid4()
        job = JOB_RESPONSE(
            job_id=id,
            song=i.song
        )
        jobs.append(job)

    for i in jobs: PROCESS_QUE.put(i)

    return {
        "success": True,
        "Message": "created requests",
        "data": jobs
    }

@app.get("/download/{job_id}")
async def download_file(job_id):
    print(job_id)
    return FileResponse(
        path=f"{Path(FINISHED_DIR/ "Adele - Hello.mp3")}",
        filename="test",
        content_disposition_type="inline"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api_settings["port"],
        host=api_settings["host"],
        reload=True,
        use_colors=True
    )
