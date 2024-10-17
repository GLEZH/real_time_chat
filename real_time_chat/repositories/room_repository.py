from sqlalchemy.orm import Session

from real_time_chat.models.room import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Room).all()

    def create_room(self, name: str):
        room = Room(name=name)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def get_by_name(self, name: str):
        return self.db.query(Room).filter(Room.name == name).first()
