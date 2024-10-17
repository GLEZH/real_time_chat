from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from real_time_chat.schemas.users import UserRead
from real_time_chat.config import settings
from real_time_chat.repositories.user_repository import UserRepository
from real_time_chat.database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_repository(db=Depends(get_db)):
    return UserRepository(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
