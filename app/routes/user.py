from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, Depends, status
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File
from neo4j.work.simple import Session
from starlette.responses import HTMLResponse, JSONResponse
from helpers.image_upload import upload_image
from helpers.emails import send_email
from helpers.auth import get_password_check, gen_token, decode_token, get_password_hash, verify_token
from config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from cypher.user import CREATE_USER, DELETE_USER, EDIT_USER, GET_USER_BY_USERNAME, GET_USERS, GET_USER_RECOMMENDATION
from models.user import UserSchema, UpdateUserModel
from fastapi.templating import Jinja2Templates
from db.neo4j import get_db
from datetime import timedelta, datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.get("/recommendation", response_description="Users retrieved")
async def get_users_recommendation(username: Optional[str] = None, session: Session = Depends(get_db)):
    if username:
        result = session.run(GET_USER_RECOMMENDATION, {'username': username})
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Post of {username} not found")
    else:
        return JSONResponse(content=[])

@router.get("/users", response_description="Users retrieved")
async def get_users(username: Optional[str] = None, session: Session = Depends(get_db)):
    if username:
        result = session.run(GET_USER_BY_USERNAME, {'username': username})
        for i in result:
            data = dict(i['n']) 
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"{username} not found")
    else:
        result = session.run(GET_USERS)
        data = [dict(i['n']) for i in result]
        if data is not None:
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail=f"Error retrieving data")


@router.post("/registration", response_description="User Registration")
async def create_user(session: Session = Depends(get_db), user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user['password'] = get_password_hash(user['password'])
    result = session.run(CREATE_USER, {'user': user})
    data = [dict(i['n']) for i in result]
    if data is not None:
        await send_email([user['email']], user)
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while creating user")

@router.patch("/", response_description="User Registration")
async def edit_user(username: str, session: Session = Depends(get_db), user: UpdateUserModel = Body(...)):
    user = jsonable_encoder(user, exclude_none=True)
    print(user)
    result = session.run(EDIT_USER, {'user': dict(user), 'username': username})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=data)
    raise HTTPException(status_code=404, detail=f"Error while updating post")


@router.delete("/", response_description="User data deleted from the database")
async def delete_user(username: str, session: Session = Depends(get_db)):
    result = session.run(DELETE_USER, {'username': username})
    data = [dict(i['n']) for i in result]
    if data is not None:
        return JSONResponse(content=f"Record {username} deteled successfully!")
    raise HTTPException(status_code=404, detail=f"Record {username} not found")



templates = Jinja2Templates(directory="app/static/html")
@router.get("/verification", response_description="Email verification", response_class=HTMLResponse)
async def verify_user(token: str, session: Session = Depends(get_db)):
    user = await verify_token(token, session)
    try:
        if user and user['is_verified'] is not True:
            user['is_verified'] = True
            result = session.run(EDIT_USER, {'user': dict(user), 'username': user['username']})
            for i in result:
                user = dict(i['n'])
            return templates.TemplateResponse("verification.html", {"username": user['username'], "host": settings.EXTERNAL_HOST, "port": settings.EXTERNAL_PORT, "endpoint": ""})
    except:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED, 
                detail = "Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
       
async def authenticate_user(username: str, password: str, session: Session = Depends(get_db)):
    result = session.run(GET_USER_BY_USERNAME, {'username': username})
    for i in result:
        user = dict(i['n'])
    password_check = await get_password_check(password, user['password'])
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User doesn't exist!",headers={"WWW-Authenticate": "Bearer"})
    elif password_check == False:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid username or password",headers={"WWW-Authenticate": "Bearer"})
    elif user['is_verified'] == False:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Please verified you email!",headers={"WWW-Authenticate": "Bearer"})
    return user

@router.post("/token", response_description="Users retrieved")
async def login(formdata: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    print(formdata.username)
    user = await authenticate_user(formdata.username, formdata.password, session)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password. Please login again!",headers={"WWW-Authenticate": "Bearer"},)
    else: 
        exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = await gen_token({"username": user['username'], "exp": exp})
        return {"access_token": token, 'token_type': 'bearer'} 


async def get_current_user(session: Session = Depends(get_db) ,token: str = Depends(oauth2_scheme)):
    print(token)
    try:
        payload = await decode_token(token)
        result = session.run(GET_USER_BY_USERNAME, {'username': payload.get('username')})
        for i in result:
            user = dict(i['n'])
        print(user)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token or expired')
    return user

@router.get('/me', response_model=UserSchema)
async def user_get_me(user: UserSchema = Depends(get_current_user)):
    return user

@router.post("/image")
async def upload_user_image(session: Session = Depends(get_db), files: List[UploadFile] = File(...), username: str = None):
    for file in files:
        paths = await upload_image(file)
    result = session.run(GET_USER_BY_USERNAME, {'username': username})
    for i in result:
        user = dict(i['n'])

    print(user)        
    
    if user['username']:
        print(user['avatar'])
        user['avatar'] = paths
        print(user['avatar'])
        result = session.run(EDIT_USER, {'user': dict(user), 'username': username})
    
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"status": "ok", "filename": paths}