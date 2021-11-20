from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_verified: bool = Field(default=False)
    avatar: str = Field(default='')
    bio: str = Field(default='')
    name: str = Field(default='')
    following: int = Field(default=0)
    follower: int = Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "username": "ntt",
                "email": "tin@gmail.com",
                "password": "123456",
            }
        }

class UserLoginType(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_verified: Optional[bool]
    avatar: Optional[str]
    bio: Optional[str]
    name: Optional[str]
    following: Optional[int]
    follower: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "username": "ntt",
                "email": "jdoe@x.edu.ng",
                "password": "123456",
                "bio": "",
                "name": "",
                "following": 0,
                "follower": 0
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


