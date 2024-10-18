
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm

from real_time_chat.services.auth_service import AuthService
from real_time_chat.containers import Container
from real_time_chat.schemas.users import UserCreate, UserRead
from real_time_chat.schemas.token import Token


router = APIRouter()

@router.post("/register", response_model=UserRead)
@inject
def register(
    user_create: UserCreate,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user = auth_service.register_user(user_create)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return user


@router.post("/login", response_model=Token)
@inject
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
