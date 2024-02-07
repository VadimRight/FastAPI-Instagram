from datetime import datetime, timezone, timedelta
from typing import Annotated

from asyncpg import UniqueViolationError
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
import jwt
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import CreateUserSchema, UserSchema, UserBaseSchema, TokenData, UserInDB
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


async def get_user_in_db_schema(session: AsyncSession, username: str) -> UserInDB:
    async with session.begin():
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar()
        if username is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {username} username")
        return UserInDB(**user.__dict__)


async def get_user_by_username(session: AsyncSession, username: str) -> UserSchema:
    async with session.begin():
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {username} username")
        return UserSchema(**user.__dict__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user_in_db_schema(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
        # if username is None:
        #     raise credentials_exception
    token_data = TokenData(username=username)
    # except jwt.PyJWTError:
    #     raise credentials_exception
    user: User = await get_user_by_username(session, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    return user
