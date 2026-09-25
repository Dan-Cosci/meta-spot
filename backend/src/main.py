
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core import api_settings, client_store, cors_settings, thread_settings
from core.config import PROCESS_QUE
from routes import music_router, process_router
from worker import delete_worker, worker

WORKER_THREADS: list = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("process start")
    # print(api_settings,cors_settings)

    stop = threading.Event()

    # adding the workers
    for i in range(thread_settings["max_threads"]):
        client_store.register(i)
        WORKER_THREADS.append(threading.Thread(target=worker, args=(i, PROCESS_QUE, stop), name=f"worker: {i}"))

    # adding the delete worker
    WORKER_THREADS.append(threading.Thread(target=delete_worker, args=(67,stop,), name="delete worker: 67"))

    # spotifyClient for data requesting
    client_store.register(worker_id=77)

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


app.include_router(process_router)
app.include_router(music_router)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api_settings["port"],
        host=api_settings["host"],
        reload=api_settings["env"] == "development",
        use_colors=True
    )
