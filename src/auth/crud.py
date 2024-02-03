from typing import Any, Annotated

from asyncpg import UniqueViolationError
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from starlette import status
import jwt
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import CreateUserSchema, UserSchema, UserBaseSchema, TokenData
from src.config import SECRET, ALGORITHM
from src.database import get_session
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


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    async with session.begin():
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar()


async def get_user_by_id(session: AsyncSession, id: int) -> str | User | None:
    async with session.begin():
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        if id is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {id} id")
        return result.scalar()


async def get_user_by_username(session: AsyncSession, username: str) -> UserBaseSchema:
    async with session.begin():
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar()
        if username is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {username} username")
        return UserBaseSchema(**user.__dict__)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
        # if username is None:
        #     raise credentials_exception
    token_data = TokenData(email=email)
    # except jwt.PyJWTError:
    #     raise credentials_exception
    user = await get_user_by_email(session, email=token_data.email)
    # if user is None:
    #     raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
