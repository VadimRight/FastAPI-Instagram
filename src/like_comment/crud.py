from uuid import uuid4
from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.like_post.schemas import LikeCommentSchema
from src.models.models import Like_For_Comment
from src.verif import get_id_from_token
from src.auth.oauth import oauth2_scheme

async def create_like_post(post_id, session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    async with session.begin():
        user_id = get_id_from_token(token)
        like_for_post = Like_For_Comment(id = uuid4, user_id = user_id, post_id = post_id)
        session.add(like_for_post)
        await session.flush
        await session.refresh(like_for_post)
        return LikeCommentSchema.model_validate(like_for_post)
    

async def delete_like_post(post_id, session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    async with session.begin():
        query = delete(Like_For_Comment).where(post_id == post_id)
        await session.execute(query)
