from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from src.auth.auth import create_user, get_user
from src.auth.schemas import UserSchema, CreateUserSchema, UserLoginSchema
from src.database import get_session
from src.models.models import User

router = APIRouter()


@router.post('/login', response_model=Dict)
async def signup(
        payload: UserLoginSchema = Body(),
        session: AsyncSession = Depends(get_session)
):
    user: User = await get_user(session=session, email=payload.email)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Invalid user credentials"
        )
    is_validated: bool = user.validate_password(payload.hashed_password)
    if not is_validated:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


@router.get("/profile/{id}")
async def profile(id: int, session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail=f"There is no such user with id {id}", )
    return {"user": user}


@router.post("/register")
async def register(payload: CreateUserSchema = Body(),
                   session: AsyncSession = Depends(get_session)):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)
