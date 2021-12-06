from pydantic import BaseModel, Field

class MessageContent(BaseModel):
    content: str = Field(default='')
    username: str = Field(default='')

    class Config:
        schema_extra = {
            "example": {
                "content": "",
                "username": "",
            }
        }


