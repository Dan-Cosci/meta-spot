
from fastapi import FastAPI
from fastapi.routing import JSONResponse
from core import api


app = FastAPI()

@app.get("/")
async def hello():
    return JSONResponse({"success": True, "Message": "Hello from fastapi"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        port=api["port"],
        host=api["host"],
        reload=True,
        use_colors=True
    )
