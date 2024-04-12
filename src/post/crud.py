from typing import Annotated
from uuid import uuid4

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.oauth import oauth2_scheme
from src.auth.schemas import TokenData
from src.database import get_session
from src.post.schemas import PostCreate, PostSchema
from src.models.models import Post, User
from src.verif import get_id_from_token, verify_owner
from fastapi import UploadFile

async def create_post(name, text, post_image: UploadFile, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    try:
        async with session.begin():
            user_id = await get_id_from_token(token)
            image = Post(id = uuid4(), text=text, image=post_image, name=name, user_id=user_id)
            session.add(image)
            await session.flush() 
            await session.refresh(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")
    

async def get_post_by_username(session: AsyncSession, username: str):
    async with session.begin():
        query = select(Post).join(User).where(User.username == username)
        result = await session.execute(query)
        posts = result.scalars()
        if posts == []:
            return {"detail": "User hasn't post anything yet"}
        return (post for post in posts)

    
async def get_post_by_id(session: AsyncSession, id: str):
    async with session.begin():
        query = select(Post).where(Post.id == id)
        result = await session.execute(query)
        post = result.scalar()
        if post is None:
            raise HTTPException(status_code=400)
        return post


async def get_username_by_post_id(session: AsyncSession, id: str):
        async with session.begin():
            query = select(User.username).where(User.id == Post.user_id)
            result = await session.execute(query)
            username = result.scalar
            if username is None:
                raise HTTPException(status_code=404)
            return username

async def get_my_post(session: AsyncSession, token: str):
    try:
        async with session.begin():
            id = await get_id_from_token(token)
            token_data = TokenData(id=id)
            query = select(Post).join(User).where(User.id == token_data.id)
            result = await session.execute(query)
            my_images = result.scalars()
            if my_images == []:
                return {"detail": "You haven't posted anything yet"}
            return (image for image in my_images)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")


async def delete_my_post(session: AsyncSession, id: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = delete(Post).where(Post.id == id)
        await session.execute(query)


async def edit_post_name(session: AsyncSession, id: str, name: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(Post).where(Post.id == id).values(name=name)
        await session.execute(query)


async def edit_post_image(session: AsyncSession, id: str, image: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(Post).where(Post.id == id).values(image=image)
        await session.execute(query)
