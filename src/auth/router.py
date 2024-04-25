from datetime import timedelta
from typing import Annotated, Set

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.crud import create_user, edit_user_mail, edit_user_username, get_user_by_username, authenticate_user, create_access_token, get_current_user, reset_password
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import UserResponceSchema, CreateUserResponceSchema, UserBaseSchema, Token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_session
from src.models.models import Post, User
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from src.post.crud import get_my_post, get_post_by_username
from src.science import time_decorator


# User router initialization
router = APIRouter(
    tags=["User"]
)


# Endpoint router with post request
@router.post("/register")
@time_decorator
async def register(payload: CreateUserResponceSchema = Body(),
                   session: AsyncSession = Depends(get_session)):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)


@router.get("/users/{username}")
@time_decorator
async def profile(
        username: str,
        session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    user: User = await get_user_by_username(session, username)
    await get_user_by_username(session, username)
    posts: Post = await get_post_by_username(session, username)
    return user, posts


@router.get("/profile")
@time_decorator
async def read_users_me(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user: User = await get_current_user(token, session)
    posts: Set[Post] = await get_my_post(session, token)
    return user, posts


# Endpoint for user authentication and getting token
@router.post("/token")
@time_decorator
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
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.patch("/profile/change_username")
@time_decorator
async def update_username(username: str, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await edit_user_username(session, username, token)



@router.patch("/profile/change_email/")
@time_decorator
async def update_email(email: str, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await edit_user_mail(session, email, token)



@router.patch("/profile/reset_passwd")
@time_decorator
async def update_passwd(passwd: str, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await reset_password(session, passwd, token)
