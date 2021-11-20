from typing import List, Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class RoomSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(default='')
    cover: str = Field(default='')
    last_active: datetime = Field(default=datetime.utcnow())
    at: datetime = Field(default=datetime.utcnow())

    class Config:
        schema_extra = {
            "example": {
                "name": "",
                "cover": "",
            }
        }


class MutateRoomModel(BaseModel):
    name: Optional[str]
    cover: Optional[str]
    last_active: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "name": "",
                "cover": '',
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }
    
