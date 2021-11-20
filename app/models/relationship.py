import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class FOLLOWS(BaseModel):
    since: datetime = Field(default=datetime.utcnow())

class HAS_COMMENT(BaseModel):
    since: datetime = Field(default=datetime.utcnow())

class IS_AUTHOR(BaseModel):
    since: datetime = Field(default=datetime.utcnow())

class IS_COMMENTATOR(BaseModel):
    since: datetime = Field(default=datetime.utcnow())

class RECEIVED_POST_LIKE(BaseModel):
    since: datetime = Field(default=datetime.utcnow())

class RECEIVED_COMMENT_LIKE(BaseModel):
    since: datetime = Field(default=datetime.utcnow())