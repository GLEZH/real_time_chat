from real_time_chat.repositories.message_repository import MessageRepository
from real_time_chat.repositories.room_repository import RoomRepository
from real_time_chat.repositories.user_repository import UserRepository
from real_time_chat.schemas.room import RoomCreate


class ChatService:
    def __init__(
        self,
        message_repo: MessageRepository,
        room_repo: RoomRepository,
        user_repo: UserRepository,
    ):
        self.message_repo = message_repo
        self.room_repo = room_repo
        self.user_repo = user_repo


    def get_all_rooms(self):
        return self.room_repo.get_all()


    def create_room(self, room_create: RoomCreate):
        return self.room_repo.create_room(room_create.name)


    def get_room_by_name(self, name: str):
        return self.room_repo.get_by_name(name)


    def save_message(self, room_id: int, user_id: int, content: str):
        return self.message_repo.create_message(room_id, user_id, content)
