from dependency_injector import containers, providers

from real_time_chat.repositories.user_repository import UserRepository
from real_time_chat.repositories.message_repository import MessageRepository
from real_time_chat.repositories.room_repository import RoomRepository
from real_time_chat.services.auth_service import AuthService
from real_time_chat.services.chat_service import ChatService
from real_time_chat.database import SessionLocal


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["real_time_chat.api.auth", "real_time_chat.api.chat", "real_time_chat.main"]
    )

    db_session = providers.Factory(SessionLocal)

    user_repository = providers.Factory(
        UserRepository,
        db=db_session,
    )

    message_repository = providers.Factory(
        MessageRepository,
        db=db_session,
    )

    room_repository = providers.Factory(
        RoomRepository,
        db=db_session,
    )

    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
    )

    chat_service = providers.Factory(
        ChatService,
        message_repo=message_repository,
        room_repo=room_repository,
        user_repo=user_repository,
    )
