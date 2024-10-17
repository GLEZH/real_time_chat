# app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from typing import List

from real_time_chat.services.chat_service import ChatService
from real_time_chat.containers import Container
from real_time_chat.schemas.room import RoomCreate, RoomRead
from real_time_chat.dependencies import get_current_user
from real_time_chat.models.user import User


router = APIRouter()

@router.get("/rooms", response_model=List[RoomRead])
@inject
def get_rooms(
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    current_user: User = Depends(get_current_user),
):
    return chat_service.get_all_rooms()


@router.post("/rooms", response_model=RoomRead)
@inject
def create_room(
    room_create: RoomCreate,
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    current_user: User = Depends(get_current_user),
):
    existing_room = chat_service.get_room_by_name(room_create.name)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room already exists",
        )
    return chat_service.create_room(room_create)
