from uuid import uuid4
from asyncpg import NotNullViolationError
from fastapi import Depends, HTTPException
from sqlalchemy import delete, select
from src.comment.schemas import CommentCreate, CommentShema
from src.database import get_session
from src.models.models import Comment, Post
from src.post.schemas import PostSchema
from src.verif import get_id_from_token, verify_owner_comment
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.oauth import oauth2_scheme



async def create_comment(posts_id, payload: CommentCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> PostSchema:
    try:
        async with session.begin():
            user_id = await get_id_from_token(token)            
            # token_data = TokenData(id=id)
            comment = Comment(id = uuid4(), text=payload.text, user_id=user_id, post_id=posts_id)
            print(comment)
            session.add(comment)
            await session.flush()  
            await session.refresh(comment)
            return CommentShema.model_validate(comment)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")
    

async def get_comments_by_post_id(session: AsyncSession, post_id: str):
    async with session.begin():
        query = select(Comment).where(Comment.post_id == post_id)
        result = await session.execute(query)
        comments = result.scalars()
        if comments == []:
            return  {"details": "There no any comments yet"}
        return [comment for comment in comments]



async def delete_my_comment(session: AsyncSession, id: str, token: str):
    owner = await verify_owner_comment(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = delete(Post).where(Post.id == id)
        await session.execute(query)
        