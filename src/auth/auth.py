from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from src.auth.schemas import CreateUserSchema, UserSchema
from src.database import SessionLocal
from src.models.models import User


async def create_user(session: AsyncSession, payload: CreateUserSchema) -> UserSchema:
    try:
        async with session.begin():
            user = User(username=payload.username, email=payload.email, hashed_password=payload.hashed_password)
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return UserSchema.model_validate(user)
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Username or email already registered")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")