
import threading
from contextlib import asynccontextmanager
from queue import Queue
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from core import FINISHED_DIR, api_settings, store
from models import JOB_REQUEST, JOB_RESPONSE
from worker import worker

PROCESS_QUE: Queue = Queue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("process start")

    stop = threading.Event()
    threads = [
        threading.Thread(target=worker, args=(i, PROCESS_QUE, stop), name=f"worker: {i}")
        for i in range(3)
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
    file = [i for i in FINISHED_DIR.glob(f"*_{job_id}.mp3")]

    return FileResponse(
        path=file[0],
        filename=str(str(file[0].name).split("_")[0]+ "."+str(file[0].name).split(".")[1]),
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
