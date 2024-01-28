from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.auth.auth import create_user
from src.auth.schemas import UserSchema, CreateUserSchema
from src.database import get_session, SessionLocal
from src.models.models import User

router = APIRouter()


@router.post('/signup', response_model=UserSchema)
async def signup(
        payload: CreateUserSchema = Body(),
        session: AsyncSession = Depends(get_session)
):
    """Processes request to register user account."""
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return await create_user(session, payload)


# async def get_user_by_id(session:AsyncSession, id: int):
#     result = await session.execute(select(User.id == id))
#     return result.scalar().all()


@router.get("/profile/{id}")
async def profile(session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    result = await session.execute(select(User))
    return {"user": result.mappings().all()}
