from fastapi import APIRouter, HTTPException, Depends
from neo4j.work.simple import Session
from starlette.responses import JSONResponse
from cypher.comment import EDIT_COMMENT
from cypher.post import EDIT_POST, GET_USERS_LIKED_POST, GET_USERS_LIKED_COMMENT, GET_POST_BY_ID
from cypher.user import FOLLOW_USER, LIKE_COMMENT, LIKE_POST, UNFOLLOW_USER, UNLIKE_COMMENT, UNLIKE_POST, GET_USER_FOLLOWER, GET_USER_FOLLOWING, EDIT_USER, JOIN_ROOM, LEAVE_ROOM
from datetime import datetime
from db.neo4j import get_db

router = APIRouter()

@router.post("/follow", response_description="User follows another user")
async def follow(session: Session = Depends(get_db), me: str = None, you: str = None):
    result = session.run(FOLLOW_USER, {'me': me, 'you': you, 'since': str(datetime.utcnow())})
    data = [dict(i['r']) for i in result]
    following_result = session.run(GET_USER_FOLLOWING, {'username': me})
    following = [(i['following']) for i in following_result]
    follower_result = session.run(GET_USER_FOLLOWER, {'username': me})
    follower = [(i['follower']) for i in follower_result]
    result = session.run(EDIT_USER, {'user': dict({'following': len(following), 'follower': len(follower)}), 'username': me})
    if data is not None:
        return JSONResponse(content={'message': f'{me} followed {you}!'})
    raise HTTPException(status_code=404, detail=f"Error while following")


@router.delete("/unfollow", response_description="User follows another user")
async def unfollow(session: Session = Depends(get_db), me: str = None, you: str = None):
    result = session.run(UNFOLLOW_USER, {'me': me, 'you': you})
    data = [dict(i['r']) for i in result]
    if data is not None:
        return JSONResponse(content={'message': f'{me} unfollowed {you}!'})
    raise HTTPException(status_code=404, detail=f"Error while unfollowing")


@router.post("/likepost", response_description="User follows another user")
async def like_post(session: Session = Depends(get_db), username: str = None, post_id: str = None):
    result = session.run(LIKE_POST, {'username': username, 'post_id': post_id, 'since': str(datetime.utcnow())})
    data = [dict(i['r']) for i in result]
    users_liked_post = session.run(GET_USERS_LIKED_POST, {'post_id': post_id})
    users = [(i['userlike']) for i in users_liked_post]
    print(users)
    session.run(EDIT_POST, {'post': dict({'like_count': len(users)}), 'id': post_id})
    
    
    if data is not None:
        result = session.run(GET_POST_BY_ID, {'id': post_id})
        data = [dict(i['n']) for i in result]     
        if data is not None:
            return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while liking")


@router.delete("/unlikepost", response_description="User follows another user")
async def unlike_post(session: Session = Depends(get_db), username: str = None, post_id: str = None):
    result = session.run(UNLIKE_POST, {'username': username, 'post_id': post_id})
    data = [dict(i['r']) for i in result]
    users_liked_post = session.run(GET_USERS_LIKED_POST, {'post_id': post_id})
    users = [(i['userlike']) for i in users_liked_post]
    print(users)
    session.run(EDIT_POST, {'post': dict({'like_count': len(users)}), 'id': post_id})
    if data is not None:
        return JSONResponse(content={'message': f'{username} unliked post {post_id}!'})
    raise HTTPException(status_code=404, detail=f"Error while unliking")


@router.post("/likecomment", response_description="User follows another user")
async def like_comment(session: Session = Depends(get_db), username: str = None, comment_id: str = None):
    result = session.run(LIKE_COMMENT, {'username': username, 'comment_id': comment_id, 'since': str(datetime.utcnow())})
    data = [dict(i['r']) for i in result]
    users_liked_comment = session.run(GET_USERS_LIKED_COMMENT, {'comment_id': comment_id})
    users = [(i['userlike']) for i in users_liked_comment]
    print(users)
    session.run(EDIT_COMMENT, {'comment': dict({'comment_like_count': len(users)}), 'id': comment_id})
    if data is not None:
        return JSONResponse(content={'message': f'{username} liked comment {comment_id}!'})
    raise HTTPException(status_code=404, detail=f"Error while liking")


@router.delete("/unlikecomment", response_description="User follows another user")
async def unlike_comment(session: Session = Depends(get_db), username: str = None, comment_id: str = None):
    result = session.run(UNLIKE_COMMENT, {'username': username, 'comment_id': comment_id})
    data = [dict(i['r']) for i in result]
    users_liked_comment = session.run(GET_USERS_LIKED_COMMENT, {'comment_id': comment_id})
    users = [(i['userlike']) for i in users_liked_comment]
    print(users)
    session.run(EDIT_COMMENT, {'comment': dict({'comment_like_count': len(users)}), 'id': comment_id})
    if data is not None:
        return JSONResponse(content={'message': f'{username} unliked comment {comment_id}!'})
    raise HTTPException(status_code=404, detail=f"Error while unliking")


@router.post("/joinroom", response_description="User joins a room")
async def join_room(session: Session = Depends(get_db), username: str = None, room_id: str = None):
    result = session.run(JOIN_ROOM, {'username': username, 'room_id': room_id, 'since': str(datetime.utcnow())})
    data = [dict(i['r']) for i in result]
    if data is not None:
        return JSONResponse(content={'message': f'{username} joined room {room_id}!'})
    raise HTTPException(status_code=404, detail=f"Error while joining room")


@router.delete("/leaveroom", response_description="User leaves a room")
async def leave_room(session: Session = Depends(get_db), username: str = None, room_id: str = None):
    result = session.run(LEAVE_ROOM, {'username': username, 'room_id': room_id})
    data = [dict(i['r']) for i in result]
    if data is not None:
        return JSONResponse(content={'message': f'{username} left room {room_id}!'})
    raise HTTPException(status_code=404, detail=f"Error while leaving room")