
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from queue import Queue
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from core import FINISHED_DIR, api_settings, store
from models import JOB_REQUEST, JOB_RESPONSE
from services import check_dirs
from worker import delete_worker, worker

PROCESS_QUE: Queue = Queue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("process start")
    check_dirs()

    stop = threading.Event()
    threads = [
        *[threading.Thread(target=worker, args=(i, PROCESS_QUE, stop), name=f"worker: {i}") for i in range(3)],
        threading.Thread(target=delete_worker, args=(67,stop,), name="delete worker: 67")
    ]

    for i in threads:
        i.start()

    yield

    stop.set()
    for i in threads:
        i.join(timeout=30)

    print("process ended")

app = FastAPI(lifespan=lifespan)


app.add_middleware(CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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
    file = next(iter(FINISHED_DIR.glob(f"*_{job_id}.mp3")))

    updated_job = store.get(job_id=job_id)
    if not updated_job: return { "success": False, "status_code": 404, "message": "Job id does not exist" }
    updated_job.is_downloaded = True
    updated_job.file_name = file.name
    updated_job.file_path = file
    updated_job.downloaded_at = datetime.now().timestamp()
    store.update_job(job_id, updated_job)

    return FileResponse(
        path=file,
        filename=str(str(file.name).split("_")[0]+ "."+str(file.name).split(".")[1]),
        content_disposition_type="attachment"
    )

@app.get("/status/{job_id}")
async def job_status(job_id):
    job = store.get(job_id)
    if not job: return {"success": False, "message":"job_id does not exists"}

    return {
        "job_id": job_id,
        "status" : job.status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api_settings["port"],
        host=api_settings["host"],
        reload=api_settings["env"] == "development",
        use_colors=True
    )
