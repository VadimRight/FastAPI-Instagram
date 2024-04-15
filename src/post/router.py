
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_user_by_username
from src.database import get_session
from src.auth.oauth import oauth2_scheme
from src.post.crud import create_post, delete_my_post, edit_post_image, edit_post_name, get_my_post, get_post_by_id, get_post_by_username
from src.models.models import Post
from fastapi import File, UploadFile
from src.verif import verify_user
from fastapi import HTTPException


router = APIRouter(
    tags=["Post"]
)



# Router for getting all images from specific user
@router.get("/users/{username}/posts")
async def get_image(username: str, session: AsyncSession =  Depends(get_session)):
    await get_user_by_username(session, username)
    post: Post = await get_post_by_username(session, username)
    return post


@router.get("/users/{username}/posts={id}")
async def get_spesfic_post(username: str, id: str, session: AsyncSession = Depends(get_session)):
    await get_user_by_username(session, username)
    post: Post = await get_post_by_id(session, id)
    return post

# image router with get request, which returns all images
@router.post("/new_post", status_code=201)
async def post_image(text, name, image: UploadFile = File(None), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await create_post(name, text, image, token, session)


@router.get("/profile/posts")
async def get_my_images(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    check = await verify_user(session, token)
    if not check:
        raise HTTPException(status_code = 204, detail = 'It s not yours')
    posts: Post = await get_my_post(session, token)
    return posts


@router.get("/profile/posts={id}")
async def get_spesific_post(id: str, session: AsyncSession = Depends(get_session)):
    post: Post = await get_post_by_id(session, id)
    return post


@router.delete("/profile/posts={id}")
async def delete_image( id: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await delete_my_post(session, id, token)


@router.patch("/profile/posts={id}/edit_name")
async def update_name(id: str, name: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_post_name(session, id, name, token)


@router.patch("/profile/posts={id}/edit_image")
async def upgrade_image(id: str, image: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_post_image(session, id, image, token)
