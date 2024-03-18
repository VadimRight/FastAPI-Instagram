from asyncpg import NotNullViolationError
from fastapi import Depends, HTTPException
from src.auth.schemas import TokenData
from src.comment.schemas import CommentCreate, CommentShema
from src.database import get_session
from src.models.models import Comment
from src.post.schemas import PostSchema
from src.verif import get_id_from_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.oauth import oauth2_scheme

# async def get_username_by_post_id()



async def create_comment(payload: CommentCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> PostSchema:
    try:
        async with session.begin():
            id = await get_id_from_token(token)            
            token_data = TokenData(id=id)
            image = Comment(image=payload.image, name = payload.name, user_id=token_data.id)
            session.add(image)
            await session.flush()   
            await session.refresh(image)
            return CommentShema.model_validate(image)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")


