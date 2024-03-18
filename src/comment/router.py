
from fastapi import APIRouter, Body, Depends

from src.auth.crud import get_user_by_username
from src.comment.schemas import CommentCreate
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["Comment"]
)


# @router.post("/users/{username}/posts")
# async def post_comment(payload: CommentCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    # 
    # await get_user_by_username(session, username)