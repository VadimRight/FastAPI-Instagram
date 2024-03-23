
from fastapi import APIRouter, Body, Depends

from src.auth.crud import get_user_by_username
from src.comment.crud import create_comment
from src.comment.schemas import CommentCreate
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

from src.post.crud import get_username_by_post_id


router = APIRouter(
    tags=["Comment"]
)


@router.post("/users/{username}/posts={id}")
async def post_comment(post_id, payload: CommentCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    # username = await get_username_by_post_id(session, post_id)
    # await get_user_by_username(session, username)
    return await create_comment(payload, token, session)