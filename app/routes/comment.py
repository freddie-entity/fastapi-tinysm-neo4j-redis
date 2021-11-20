from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from neo4j.work.simple import Session
from starlette.responses import JSONResponse
from cypher.post import EDIT_POST
from cypher.comment import CREATE_COMMENT, DELETE_COMMENT, EDIT_COMMENT, GET_COMMENT_BY_ID, GET_COMMENT_BY_POST_ID, GET_COMMENT_BY_USERNAME, GET_COMMENTS
from db.neo4j import get_db
from models.comment import CommentSchema, MutateCommentModel

router = APIRouter()

@router.get("/", response_description="Get a single comment")
async def get_comment(session: Session = Depends(get_db), id: Optional[str] = None, post_id: Optional[str] = None, username: Optional[str] = None):
    if id:
        result = session.run(GET_COMMENT_BY_ID, {'id': id})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Comment {id} not found")
    elif username:
        result = session.run(GET_COMMENT_BY_USERNAME, {'username': username})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Comment of username{username} not found")
    elif post_id:
        result = session.run(GET_COMMENT_BY_POST_ID, {'post_id': post_id})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Comment of post {post_id} not found")
    else: 
        result = session.run(GET_COMMENTS)
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Error retrieving data")


@router.post("/", response_description="Comment on a post")
async def create_comment(session: Session = Depends(get_db), comment: CommentSchema = Body(...)):
    comment = jsonable_encoder(comment)
    result = session.run(CREATE_COMMENT, {'comment': comment, 'username': comment['username'], 'post_id': comment['post_id'], 'since': str(datetime.utcnow())})
    comment_list = session.run(GET_COMMENT_BY_POST_ID, {'post_id': comment['post_id']})
    count = [dict(i['n']) for i in comment_list]
    session.run(EDIT_POST, {'post': dict({'comment_count': len(count)}), 'id': comment['post_id']})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while creating comment")


@router.patch("/{id}", response_description='Update a comment')
async def update_comment(id: str, session: Session = Depends(get_db), comment: MutateCommentModel = Body(...)):
    comment = jsonable_encoder(comment, exclude_none=True)
    result = session.run(EDIT_COMMENT, {'comment': dict(comment), 'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while updating comment")



@router.delete("/{id}", response_description="Comment deleted from the database")
async def delete_comment(id: str,  session: Session = Depends(get_db)):
    result = session.run(DELETE_COMMENT, {'id': id})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=f"Record {id} deteled successfully!")
    raise HTTPException(status_code=404, detail=f"Record {id} not found")
