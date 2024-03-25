from uuid import uuid4
from asyncpg import NotNullViolationError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Like_For_Post
from src.post_like.schemas import LikeSchema
from src.verif import get_id_from_token



async def create_like(token: str, session: AsyncSession, post_id: str):
    try:
        async with session.begin():
            user_id = await get_id_from_token(token)
            like = Like_For_Post(id = uuid4(), user_id = user_id, post_id = post_id)
            session.add(like)
            await session.flush()
            await session.refresh(like)
            return LikeSchema.model_validate(like)
        
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")


