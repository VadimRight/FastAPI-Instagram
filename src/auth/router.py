from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from src.auth.auth import create_user, get_user, get_user_by_id
from src.auth.schemas import UserSchema, CreateUserSchema, UserLoginSchema
from src.database import get_session
from src.models.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# setup authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()


@router.post('/login', response_model=Dict)
async def signup(
        payload: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user: User = await get_user(session=session, email=payload.username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Invalid user credentials"
        )
    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


@router.get("/profile/{id}")
async def profile(id: int,
                  token: str = Depends(oauth2_scheme),
                  session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    user: User = await get_user_by_id(session, id)
    return user


@router.post("/register")
async def register(payload: CreateUserSchema = Body(),
                   session: AsyncSession = Depends(get_session)):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)
