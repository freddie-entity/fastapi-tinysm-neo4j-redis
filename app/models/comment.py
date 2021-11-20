from typing import List, Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class CommentSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    username: str = Field(...)
    post_id: str = Field(...)
    content: str = Field(default='')
    comment_like_count: int = Field(default=0) # List user
    at: datetime = Field(default=datetime.utcnow())

    class Config:
        schema_extra = {
            "example": {
                "username": "ntt",
                "post_id": '8923fj0234',
                "content": "Waterresourcesengineering",
            }
        }


class MutateCommentModel(BaseModel):
    content: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "content": "Waterresources",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }
    
