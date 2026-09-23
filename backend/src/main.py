
import asyncio
import threading
from contextlib import asynccontextmanager
from queue import Full, Queue
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from core import FINISHED_DIR, api_settings, cors_settings, store, thread_settings
from models import JOB_REQUEST, JOB_RESPONSE
from services import check_dirs
from utils import get_current_timestamp
from worker import delete_worker, worker

PROCESS_QUE: Queue = Queue(maxsize=thread_settings["max_que"])
WORKER_THREADS: list = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("process start")
    # print(api_settings,cors_settings)
    check_dirs()

    stop = threading.Event()

    # adding the workers
    [
        WORKER_THREADS.append(threading.Thread(target=worker, args=(i, PROCESS_QUE, stop), name=f"worker: {i}"))
        for i in range(thread_settings["max_threads"])
    ]

    # adding the delete worker
    WORKER_THREADS.append(threading.Thread(target=delete_worker, args=(67,stop,), name="delete worker: 67"))

    for i in WORKER_THREADS:
        i.start()

    yield

    stop.set()
    for i in WORKER_THREADS:
        i.join(timeout=30)

    print("process ended")

app = FastAPI(lifespan=lifespan)


app.add_middleware(CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_settings["allowed_origins"],
    allow_methods=cors_settings["allowed_methods"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)



@app.get("/health")
def health():
    thread_count = sum(1 for t in WORKER_THREADS if t.is_alive())
    worker_health = thread_count == len(WORKER_THREADS)


    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "checks": {
                "active_workers": thread_count,
                "workers_health": worker_health
            }
        }
    )

@app.post("/job")
async def create_job(req: JOB_REQUEST):
    id = uuid4()
    job = JOB_RESPONSE(
        job_id=id,
        song=req.song
    )

    deadline = asyncio.get_event_loop().time() + 5
    while True:
        try:
            PROCESS_QUE.put_nowait(job)
            return JSONResponse(status_code=201, content={
                "success": True,
                "Message": "Created request",
                "data": job.model_dump(mode="json")
            })
        except Full:
            if asyncio.get_event_loop().time() >= deadline:
                return JSONResponse(status_code=503, headers={"Retry-After": "5"},
                    content={
                        "success": False,
                        "Message": "Queue is full, try again later"
                    })
            await asyncio.sleep(0.25)


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

    return JSONResponse(status_code=201, content={
        "success": True,
        "Message": "created requests",
        "data": [j.model_dump(mode="json") for j in jobs]
    })

@app.get("/download/{job_id}")
async def download_file(job_id):
    job = store.get(job_id=job_id)
    if not job:
        return JSONResponse(status_code=404, content={"success": False, "message": "Job id does not exist"})

    files = [f for f in FINISHED_DIR.glob(f"*_{job_id}.mp3")]
    if not files:
        return JSONResponse(status_code=404, content={"success": False, "message": "File not found"})

    file = files[0]
    job.is_downloaded = True
    job.downloaded_at = get_current_timestamp()
    store.update_job(job_id=job_id, item=job)

    return FileResponse(
        path=file,
        filename=job.file_name or file.name,
        content_disposition_type="attachment"
    )

@app.get("/status/{job_id}")
async def job_status(job_id):
    job = store.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"success": False, "message": "job_id does not exist"})

    return JSONResponse(content={
        "job_id": job_id,
        "status": job.status.value
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api_settings["port"],
        host=api_settings["host"],
        reload=api_settings["env"] == "development",
        use_colors=True
    )
