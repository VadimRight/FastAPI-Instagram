
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_user_by_username
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from src.post.crud import create_post, delete_my_post, edit_post_image, edit_post_name, get_my_post, get_post_by_username
from src.post.schemas import PostCreate
from src.models.models import Post


router = APIRouter(
    tags=["Post"]
)



# Router for getting all images from specific user
@router.get("/users/{username}/posts")
async def get_image(username: str, session: AsyncSession =  Depends(get_session)):
    await get_user_by_username(session, username)
    posts: Post = await get_post_by_username(session, username)
    return posts


@router.get("/users/{username}/posts={id}")
async def get_spesfic_post(username: str, session: AsyncSession = Depends(get_session)):
    await get_user_by_username(session, username)
    

# image router with get request, which returns all images
@router.post("/new_post")
async def post_image(payload: PostCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await create_post(payload, token, session)


@router.get("/profile/posts")
async def get_my_images(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    images: Post = await get_my_post(session, token)
    return images


@router.delete("/profile/posts")
async def delete_image( id: int, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await delete_my_post(session, id, token)


@router.patch("/profile/posts={id}/edit_name")
async def update_name(id: int, name: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_post_name(session, id, name, token)


@router.patch("/profile/posts={id}/edit_image")
async def upgrade_image(id: int, image: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_post_image(session, id, image, token)
