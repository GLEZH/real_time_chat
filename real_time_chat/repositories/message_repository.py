from sqlalchemy.orm import Session
from datetime import datetime

from rereal_time_chat.models.message import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, room_id: int, user_id: int, content: str):
        message = Message(
            room_id=room_id,
            user_id=user_id,
            content=content,
            timestamp=datetime.utcnow(),
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_by_room(self, room_id: int):
        return self.db.query(Message).filter(Message.room_id == room_id).all()
