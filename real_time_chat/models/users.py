# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from real_time_chat.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    messages = relationship("Message", back_populates="user")
