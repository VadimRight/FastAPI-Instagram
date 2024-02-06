
from typing import Annotated

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_current_user
from src.auth.oauth import oauth2_scheme
from src.img_logic.schemas import ImageCreate, ImageSchema
from src.models.models import User, Image


async def create_image(payload: ImageCreate, session: AsyncSession):
    try:
        async with session.begin():
            user_id: User.id = await get_current_user(Depends(oauth2_scheme))
            image = Image(image=payload.image, user_id=user_id)
            session.add(image)
            await session.flush()
            await session.refresh(image)
            return ImageSchema.model_validate(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")