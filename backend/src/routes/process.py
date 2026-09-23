from fastapi.responses import JSONResponse
from fastapi import APIRouter


router = APIRouter(prefix="/process")


@router.get("/")
async def hello():
    return JSONResponse({
        "success": True,
        "message": "Welcome to process"
    })
