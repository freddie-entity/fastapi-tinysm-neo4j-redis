from typing import List, Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class PostSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    username: str = Field(...)
    comment_count: int = Field(default=0)
    content: str = Field(default='')
    location: str = Field(default='')
    tags: List[str] = Field(default=[]) # 1 to Many username 
    archived : bool = Field(default=False)
    like_count: int = Field(default=0)
    images: List[str] = Field([]) # 1 to Many image
    at: datetime = Field(default=datetime.utcnow())

    class Config:
        schema_extra = {
            "example": {
                "username": "ntt",
                "content": "Waterresourcesengineering",
                "location": 'New York',
                "tags": [],
                "archived": False,
                "images": [],
            }
        }


class MutatePostModel(BaseModel):
    content: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]
    archived: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "content": "Waterresourcesengineering",
                "location": 'New York',
                "tags": [],
                "archived": False,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }
    
