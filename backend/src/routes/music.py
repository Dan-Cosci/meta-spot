import json

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from core import client_store

router = APIRouter(prefix="/music")

@router.get("/")
async def hello():

    return JSONResponse({
        "success": True,
        "message": "Welcome to spotify"
    })

@router.get("/data/{id}")
async def get_track_data(
    id: str,
    type:str
):

    if not type: return JSONResponse({
        "success": False,
        "message": "Parameter 'type' was not defined",
    })

    client = client_store.get(77)

    if type == "track": data = client.get_track(id)
    if type == "artist": data = client.get_artist(id)

    return JSONResponse({
        "success": True,
        "message": f"{type} data success",
        "data" : data.to_dict()
    })





@router.get("/search")
async def search(q, limit = 10 ):
    query = str(q)
    client = client_store.get(77)
    items = client.search(query=query, types=("track","artist"), limit=limit)

    print(q,type)

    return JSONResponse({
        "success": True,
        "message": "Data request success",
        "data": items.to_dict()
    })
