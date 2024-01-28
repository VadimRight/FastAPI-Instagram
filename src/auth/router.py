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


def get_user_by_id(session:AsyncSession, id:int):
    result =  session.execute(select(User)).filter(User.id == id).one()


@router.get("/profile/{id}", response_model=UserSchema)
async def profile(id: int, session: AsyncSession = Depends(get_session)):
    """Processes request to retrieve user profile by id"""
    user = await get_user_by_id(session=session, id=id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
