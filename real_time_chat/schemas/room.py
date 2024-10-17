# app/schemas/room.py
from pydantic import BaseModel


class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

    class Config:
        orm_mode = True
