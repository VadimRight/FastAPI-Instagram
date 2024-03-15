from typing import Annotated

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.oauth import oauth2_scheme
from src.auth.schemas import TokenData
from src.config import ALGORITHM, SECRET
from src.database import get_session
from src.img.schemas import ImageCreate, ImageSchema, ShowImage
from src.models.models import User, Image


async def create_image(payload: ImageCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> ImageSchema:
    try:
        async with session.begin():
            token_payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            id: int = token_payload.get("sub")
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
        return (ShowImage(**image.__dict__) for image in images)
    

async def get_my_image(session: AsyncSession, token: str):
    try:
        async with session.begin():
            token_payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            id: int = token_payload.get("sub")
            token_data = TokenData(id=id)
            query = select(Image).join(User).where(User.id == token_data.id)
            result = await session.execute(query)
            my_images = result.scalars()
            if my_images == []:
                return {"detail": "You haven't posted anything yet"}
            return (ShowImage(**image.__dict__) for image in my_images)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")




async def delete_image(session: AsyncSession):
    pass