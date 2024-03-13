from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.crud import create_user, get_user_by_username, authenticate_user, create_access_token, get_current_user
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import UserSchema, CreateUserSchema, UserBaseSchema, Token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_session
from src.models.models import User
from fastapi.security import OAuth2PasswordRequestForm

# User router initialization
router = APIRouter(
    tags=["User"]
)


# Endpoint router with post request
@router.post("/register")
async def register(payload: CreateUserSchema = Body(),
                   session: AsyncSession = Depends(get_session)):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)


@router.get("/users/{username}")
async def profile(
        username: str,
        session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    user: User = await get_user_by_username(session, username)
    return user


@router.get("/profile", response_model=UserBaseSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


# Endpoint for user authentication and getting token
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")