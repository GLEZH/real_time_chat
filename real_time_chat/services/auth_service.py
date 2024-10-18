from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

from real_time_chat.config import settings
from real_time_chat.repositories.user_repository import UserRepository
from real_time_chat.schemas.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return pwd_context.hash(password)


    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if user and self.verify_password(password, user.password):
            return user
        return None


    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


    def register_user(self, user_create: UserCreate):
        user = self.user_repo.get_by_username(user_create.username)
        if user:
            return None
        hashed_password = self.get_password_hash(user_create.password)
        return self.user_repo.create_user(user_create.username, hashed_password)
