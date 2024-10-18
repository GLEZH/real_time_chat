from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from fastapi.staticfiles import StaticFiles
from dependency_injector.wiring import inject, Provide
from jose import JWTError, jwt


from real_time_chat.api import auth, chat
from real_time_chat.containers import Container
from real_time_chat.config import settings
from real_time_chat.services.chat_service import ChatService
from real_time_chat.dependencies import get_current_user
from real_time_chat.repositories.user_repository import UserRepository


connected_users = {}

container = Container()
app = FastAPI()
app.container = Container()

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
    mount_location="/socket.io",
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
@inject
async def handle_private_message(sid, data, user_repo: UserRepository = Provide[Container.user_repository]):
    recipient_username = data["recipient_username"]
    message = data["message"]
    sender = socket_manager.get_sid_user(sid)

    recipient_user = user_repo.get_by_username(recipient_username)
    if recipient_user:
        recipient_sid = socket_manager.get_user_sid(recipient_user.id)
        if recipient_sid:
            await socket_manager.emit("private_message", {"message": message, "sender": sender.username}, room=recipient_sid)
        else:
            # Пользователь оффлайн
            pass
    else:
        # Пользователь не найден
        pass


@socket_manager.on('connect')
async def handle_connect(sid, environ, user_repo: UserRepository = Provide[Container.user_repository]):
    token = environ.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            user = user_repo.get_by_username(username)
            connected_users[sid] = user.id
        except JWTError:
            pass


@socket_manager.on('disconnect')
async def handle_disconnect(sid):
    if sid in connected_users:
        del connected_users[sid]


def get_user_id_by_sid(sid):
    return connected_users.get(sid)


def get_sid_by_user_id(user_id):
    for sid, uid in connected_users.items():
        if uid == user_id:
            return sid
    return None

app.mount("/", StaticFiles(directory="real_time_chat_frontend", html=True), name="static")

