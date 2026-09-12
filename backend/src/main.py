
from uuid import uuid4

from fastapi import FastAPI, Request
from core import api, QUE_DIR
from models import job_req, job_return
from services import write_file


app = FastAPI()

@app.get("/job/{job_id}")
async def get_job_details(job_id):
    return {
        "success": True,
        "Message": "Hello from fastapi",
        "data": job_id
    }




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
        "Message": "Created request",
        "data": job.model_dump()
    }


@app.post("/job/bulk")
async def bulk_create_job(req: list[job_req]):

    jobs = []
    for i in req:
        id = uuid4()
        job = job_return(
            job_id=id,
            song=i.song
        )
        write_file(base=QUE_DIR, file_name=f"{id}", data=job.model_dump_json())
        jobs.append(job)

    return {
        "success": True,
        "Message": "created requests",
        "data": jobs
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api["port"],
        host=api["host"],
        reload=True,
        use_colors=True
    )
