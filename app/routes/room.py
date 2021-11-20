from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from neo4j.work.simple import Session
from starlette.responses import JSONResponse
from cypher.room import CREATE_ROOM, EDIT_ROOM, GET_ROOM_BY_ID, GET_ROOMS_BY_USERNAME, GET_ROOMS, DELETE_ROOM
from db.neo4j import get_db
from models.room import RoomSchema, MutateRoomModel

router = APIRouter()

@router.get("/", response_description="Get a single room")
async def get_room(session: Session = Depends(get_db), id: Optional[str] = None, username: Optional[str] = None):
    if id:
        result = session.run(GET_ROOM_BY_ID, {'id': id})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"room {id} not found")
    elif username:
        result = session.run(GET_ROOMS_BY_USERNAME, {'username': username})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"room of username{username} not found")
    else: 
        result = session.run(GET_ROOMS)
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Error retrieving data")


@router.post("/", response_description="Create room chat")
async def create_room(session: Session = Depends(get_db), room: RoomSchema = Body(...)):
    room = jsonable_encoder(room)
    result = session.run(CREATE_ROOM, {'room': room})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while creating room")


@router.patch("/{id}", response_description='Update a room')
async def update_room(id: str, session: Session = Depends(get_db), room: MutateRoomModel = Body(...)):
    room = jsonable_encoder(room, exclude_none=True)
    result = session.run(EDIT_ROOM, {'room': dict(room), 'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while updating room")



@router.delete("/{id}", response_description="Room deleted from the database")
async def delete_room(id: str,  session: Session = Depends(get_db)):
    result = session.run(DELETE_ROOM, {'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=f"Record {id} deteled successfully!")
    raise HTTPException(status_code=404, detail=f"Record {id} not found")
