from typing import Annotated

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_id_from_token
from src.auth.oauth import oauth2_scheme
from src.auth.schemas import TokenData
from src.database import get_session
from src.img.schemas import ImageCreate, ImageSchema, ShowImage
from src.models.models import User, Image


async def verify_owner(session: AsyncSession, token: str, image_id) -> bool:
    async with session.begin():
        user_id = await get_id_from_token(token)
        print('adfgoiashnfokiasofhfoiashdfonhaosidnhfoiashfoichsadoifoiajsoifad')
        query = select(Image.user_id).where(Image.id == image_id)
        result = await session.execute(query)
        owner_id = result.scalar()
        return owner_id == user_id

async def create_image(payload: ImageCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> ImageSchema:
    try:
        async with session.begin():
            id = await get_id_from_token(token)            
            token_data = TokenData(id=id)
            image = Image(image=payload.image, name = payload.name, user_id=token_data.id)
            session.add(image)
            await session.flush()   
            await session.refresh(image)
            return ImageSchema.model_validate(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")
    

async def get_image_by_username(session: AsyncSession, username: str):
    async with session.begin():
        query = select(Image).join(User).where(User.username == username)
        result = await session.execute(query)
        images = result.scalars()
        if images == []:
            return {"detail": "User hasn't post anything yet"}
        return (image for image in images)
    

async def get_my_image(session: AsyncSession, token: str):
    try:
        async with session.begin():
            id = await get_id_from_token(token)
            token_data = TokenData(id=id)
            query = select(Image).join(User).where(User.id == token_data.id)
            result = await session.execute(query)
            my_images = result.scalars()
            if my_images == []:
                return {"detail": "You haven't posted anything yet"}
            return (image for image in my_images)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")


async def delete_my_image(session: AsyncSession, id: int, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = delete(Image).where(Image.id == id)
        await session.execute(query)

async def edit_image_name(session: AsyncSession, id: int, name: str):
    try:
        async with session.begin():
            query = update(Image).where(Image.id == id).values(name=name)
            await session.execute(query)
    except:
        pass


async def edit_image_image(session: AsyncSession, id: int, image: str):
    try:
        async with session.begin():
            query = update(Image).where(Image.id == id).values(image=image)
            await session.execute(query)
    except:
        pass