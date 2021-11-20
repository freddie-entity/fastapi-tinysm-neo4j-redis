from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, File, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from neo4j.work.simple import Session
from starlette.responses import JSONResponse
from cypher.post import CREATE_POST, DELETE_POST, EDIT_POST, GET_POST_BY_ID, GET_POST_BY_USERNAME, GET_POSTS
from db.neo4j import get_db
from models.post import PostSchema, MutatePostModel
from helpers.image_upload import upload_image

router = APIRouter()

@router.get("/", response_description="Get a single post")
async def get_post(id: Optional[str] = None, username: Optional[str] = None, turn: int = 1, session: Session = Depends(get_db)):
    limit = 3
    skip = limit*(turn-1)
    if id:
        result = session.run(GET_POST_BY_ID, {'id': id})
        data = [dict(i['n']) for i in result]     
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    elif username:
        result = session.run(GET_POST_BY_USERNAME, {'username': username, 'skip': skip, 'limit': limit})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Post of {username} not found")
    else: 
        result = session.run(GET_POSTS, {'skip': skip, 'limit': limit})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Error retrieving data")


@router.post("/", response_description="Post data added into the database")
async def create_post(session: Session = Depends(get_db), post: PostSchema = Body(...)):
    post = jsonable_encoder(post)
    result = session.run(CREATE_POST, {'post': post, 'since': str(datetime.utcnow()), 'username': post['username']})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while creating post")


@router.patch("/", response_description='Update a post')
async def update_post(id: str, session: Session = Depends(get_db), post: MutatePostModel = Body(...)):
    post = jsonable_encoder(post, exclude_none=True)
    result = session.run(EDIT_POST, {'post': dict(post), 'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while updating post")


@router.delete("/", response_description="Post data deleted from the database")
async def delete_post(id: str, session: Session = Depends(get_db)):
    result = session.run(DELETE_POST, {'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=f"Record {id} deteled successfully!")
    raise HTTPException(status_code=404, detail=f"Record {id} not found")


@router.post("/image")
async def upload_user_image(session: Session = Depends(get_db), files: List[UploadFile] = File(...), post_id: str = None):
    paths = []
    for file in files:
        paths += [await upload_image(file)]
    result = session.run(GET_POST_BY_ID, {'id': post_id})
    for i in result:
        post = dict(i['n'])
    
    if post['id']:
        print(post['images'])
        post['images'] += paths
        print(post['images'])
        result = session.run(EDIT_POST, {'post': dict(post), 'id': post_id})
    
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"status": "ok", "filename": paths}


