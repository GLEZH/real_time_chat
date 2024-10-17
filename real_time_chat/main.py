from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from real_time_chat.api import auth, chat
from real_time_chat.containers import Container
from real_time_chat.config import settings
from real_time_chat.services.chat_service import ChatService
from dependency_injector.wiring import inject, Provide


container = Container()
app = FastAPI()
app.container = container

app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/chat")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


socket_manager = SocketManager(
    app=app,
    mount_location="/ws",
    cors_allowed_origins=[],
    manager_kwargs={
        "async_mode": "asgi",
        "message_queue": f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    },
)


@socket_manager.on("join_room")
@inject
async def handle_join_room(sid, data, chat_service: ChatService = Provide[Container.chat_service]):
    room = data["room"]
    await socket_manager.enter_room(sid, room)
    await socket_manager.emit("user_joined", {"user": sid}, room=room)


@socket_manager.on("send_message")
@inject
async def handle_send_message(sid, data, chat_service: ChatService = Provide[Container.chat_service]):
    room = data["room"]
    message = data["message"]
    user_id = data["user_id"]
    chat_service.save_message(room_id=room, user_id=user_id, content=message)
    await socket_manager.emit("new_message", data, room=room)


@socket_manager.on("private_message")
async def handle_private_message(sid, data):
    recipient_sid = data["recipient_sid"]
    message = data["message"]
    await socket_manager.emit("private_message", {"message": message}, room=recipient_sid)
