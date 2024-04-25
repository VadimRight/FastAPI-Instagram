
from fastapi import APIRouter, Body, Depends

from src.comment.crud import create_comment, delete_my_comment, get_comments_by_post_id, update_comment_text
from src.comment.schemas import CommentCreate
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from src.science.time_decorator import time_decorator


router = APIRouter(
    tags=["Comment"]
)


@router.post("/users/{username}/posts={id}")
@time_decorator
async def post_comment(post_id, payload: CommentCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    # username = await get_username_by_post_id(session, post_id)
    # await get_user_by_username(session, username)
    return await create_comment(post_id, payload, token, session)


@router.get("/users/{username}/posts={id}")
@time_decorator
async def get_commts(post_id: str, session: AsyncSession = Depends(get_session)):
    return await get_comments_by_post_id(session, post_id)


@router.delete("/users/{username}/posts={id}")
@time_decorator
async def delete_commt(comment_id: str, session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    return await delete_my_comment(session, comment_id, token)

@router.patch("/users/{username}/posts={id}")
@time_decorator
async def edit_commt(comment_id: str, text: str, session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    return await update_comment_text(session, comment_id, token, text)
