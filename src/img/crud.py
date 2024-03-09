from typing import Annotated

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.oauth import oauth2_scheme
from src.auth.schemas import TokenData
from src.config import ALGORITHM, SECRET
from src.database import get_session
from src.img.schemas import ImageCreate, ImageSchema
from src.models.models import User, Image


async def create_image(payload: ImageCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    try:
        print(token)
        token_payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        id: int = token_payload.get("sub")
        token_data = TokenData(id=id)
        image = Image(image=payload.image, user_id=token_data.id)
        session.add(image)
        await session.flush()
        await session.refresh(image)
        return ImageSchema.model_validate(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")