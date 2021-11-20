from cypher.user import GET_USER_BY_USERNAME
from passlib.context import CryptContext
import jwt
from fastapi import Request, HTTPException, status, Depends
from config import settings
from neo4j.work.simple import Session
from db.neo4j import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_password_check(password, hash_password):
    return pwd_context.verify(password, hash_password)

async def verify_token(token: str, session: Session = Depends(get_db)):
    try:
        payload = await decode_token(token)
        result = session.run(GET_USER_BY_USERNAME, {'username': payload.get('username')})
        for i in result:
            user = dict(i['n'])  
    except:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def gen_token(data):
    return jwt.encode(data, settings.SECRET)

async def decode_token(token):
    return jwt.decode(token, settings.SECRET, algorithms = ['HS256'])