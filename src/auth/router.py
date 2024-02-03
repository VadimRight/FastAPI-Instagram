from datetime import timedelta
from typing import Dict, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from src.auth.crud import create_user, get_user_by_email, get_user_by_id, get_user_by_username,  \
    authenticate_user, create_access_token, get_current_user
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import UserSchema, CreateUserSchema, UserLoginSchema, UserBaseSchema, Token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_session
from src.models.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# setup authentication scheme

router = APIRouter(
    tags=["User"]

)


# @router.post('/login', response_model=Dict)
# async def signup(
#         payload: OAuth2PasswordRequestForm = Depends(),
#         session: AsyncSession = Depends(get_session)
# ):
#     user: User = await get_user_by_email(session=session, email=payload.username)
#     if user is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Invalid user credentials"
#         )
#     is_validated: bool = user.validate_password(payload.password)
#     if not is_validated:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Invalid user credentials"
#         )
#     return user.generate_token()


@router.get("/profile/{username}")
async def profile(
        username: str,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    user: User = await get_user_by_username(session, username)
    return user


@router.post("/register")
async def register(payload: CreateUserSchema = Body(),
                   session: AsyncSession = Depends(get_session)):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")