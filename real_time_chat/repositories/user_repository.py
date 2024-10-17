from sqlalchemy.orm import Session

from real_time_chat.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password: str):
        user = User(username=username, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
