from datetime import datetime, timezone, timedelta

from asyncpg import UniqueViolationError
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
import jwt
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import CreateUserResponceSchema, UserResponceSchema, TokenData, UserInDB, UserLoginSchema, UsernameSchema, UserIdShcema
from src.config import SECRET, ALGORITHM
from src.database import get_session
from src.models.models import User
from src.verif import get_id_from_token, verify_user
from uuid import uuid4

# user creation function for registration endpoint
async def create_user(session: AsyncSession, payload: CreateUserResponceSchema) -> UserResponceSchema:
    try:
        async with session.begin():
            user = User(id = uuid4(), username=payload.username, email=payload.email, hashed_password=payload.hashed_password)
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return UserResponceSchema.model_validate(user)
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Username or email already registered")


# function for getting authenticated user, which is used in code below
async def get_user_in_db_schema(session: AsyncSession, username: str) -> UserInDB:
    async with session.begin():
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar()
        if username is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {username} username")
        return UserInDB(**user.__dict__)


# Function for getting user by its username
async def get_user_by_username(session: AsyncSession, username: str) -> UserResponceSchema:
    async with session.begin():
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {username} username")
        return UserResponceSchema(**user.__dict__)


# password bcrypt instance
async def get_user_by_id(session: AsyncSession, id: int) -> UserResponceSchema:
    async with session.begin():
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        user = result.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail=f"There is no user with {id} username")
        return UserResponceSchema(**user.__dict__)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password verification function for user authentication function, which is below
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Authentication user function, which is used for user login and getting token in "token" endpoint
async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user_in_db_schema(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Token generator function, which is used in login endpoint and getting token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt



# Getting current authenticated user function
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try:
    id = await get_id_from_token(token)
        # if username is None:
        #     raise credentials_exception
    token_data = TokenData(id=id)
    # except jwt.PyJWTError:
    #     raise credentials_exception
    user: User = await get_user_by_id(session, id=token_data.id)
    # if user is None:
    #     raise credentials_exception
    return UserResponceSchema(**user.__dict__)



async def edit_user_username(session: AsyncSession, username: str, token: str):
    id = await get_id_from_token(token)
    owner = await verify_user(session, token)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(User).where(User.id == id).values(username=username)
        await session.execute(query)


async def edit_user_mail(session: AsyncSession, email: str, token: str):
    id = await get_id_from_token(token)
    owner = await verify_user(session, token)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(User).where(User.id == id).values(email=email)
        await session.execute(query)


async def delete_user(token: str, session: AsyncSession):
    id = await get_id_from_token(token)
    owner = await verify_user(session, token)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = delete(User).where(User.id == id)
        await session.execute(query)
        return {"User is deleted successfuly"}


async def reset_password(session: AsyncSession, new_passwd: str, token: str):
    id =  await get_id_from_token(token)
    owner = await verify_user(session, token)
    if owner is False:
        raise HTTPException(status_code=403, detail="Permission denied")
    async with session.begin():
        query = update(User).where(User.id ==id).values(hashed_password = User.hash_password(new_passwd))
        await session.execute(query)
