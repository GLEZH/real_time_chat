# app/schemas/message.py
from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    room_id: int


class MessageRead(MessageBase):
    id: int
    user_id: int
    timestamp: datetime


    class Config:
        orm_mode = True
