from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from real_time_chat.database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    messages = relationship("Message", back_populates="room")
