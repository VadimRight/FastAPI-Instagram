
from typing import Annotated

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_current_user
from src.auth.oauth import oauth2_scheme
from src.img.schemas import ImageCreate, ImageSchema
from src.models.models import User, Image


async def create_image(payload: ImageCreate,
                       session: AsyncSession,
                       current_user=Annotated[User, Depends(get_current_user)]
                       ):
    try:
        async with session.begin():
            image = Image(image=payload.image, user_id=current_user.id)
            session.add(image)
            await session.flush()
            await session.refresh(image)
            return ImageSchema.model_validate(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")