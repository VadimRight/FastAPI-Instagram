
from fastapi import APIRouter, Body, Depends

from src.comment.crud import create_comment, delete_my_comment, get_comments_by_post_id
from src.comment.schemas import CommentCreate
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(
    tags=["Comment"]
)


@router.post("/users/{username}/posts={id}")
async def post_comment(post_id, payload: CommentCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    # username = await get_username_by_post_id(session, post_id)
    # await get_user_by_username(session, username)
    return await create_comment(post_id, payload, token, session)


@router.get("/user/{username}/post={id}")
async def get_commts(post_id, session: AsyncSession = Depends(get_session)):
    return await get_comments_by_post_id(session, post_id)


@router.delete("/user/{username}/post={id}")
async def delete_commts(comment_id, session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    return await delete_my_comment(session, comment_id, token)

