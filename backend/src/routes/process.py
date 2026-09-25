import asyncio
from queue import Full
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from core import FINISHED_DIR, job_store
from core.config import PROCESS_QUE
from models import JOB_REQUEST, JOB_RESPONSE
from utils import get_current_timestamp

router = APIRouter(prefix="")

@router.post("/job")
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


@router.post("/job/bulk")
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

@router.get("/download/{job_id}")
async def download_file(job_id):
    job = job_store.get(job_id=job_id)
    if not job:
        return JSONResponse(status_code=404, content={"success": False, "message": "Job id does not exist"})

    files = [f for f in FINISHED_DIR.glob(f"*_{job_id}.mp3")]
    if not files:
        return JSONResponse(status_code=404, content={"success": False, "message": "File not found"})

    file = files[0]
    job.is_downloaded = True
    job.downloaded_at = get_current_timestamp()
    job_store.update_job(job_id=job_id, item=job)

    return FileResponse(
        path=file,
        filename=job.file_name or file.name,
        content_disposition_type="attachment"
    )

@router.get("/status/{job_id}")
async def job_status(job_id):
    job = job_store.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"success": False, "message": "job_id does not exist"})

    return JSONResponse(content={
        "job_id": job_id,
        "status": job.status.value
    })
