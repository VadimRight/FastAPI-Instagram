
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import get_user_by_username
from src.database import get_session
from src.img.crud import create_image, delete_my_image, edit_image_image, edit_image_name, get_image_by_username, get_my_image
from src.img.schemas import ImageCreate
from src.models.models import Image
from src.auth.oauth import oauth2_scheme


router = APIRouter(
    tags=["Image"]
)



# Router for getting all images from specific user
@router.get("/users/{username}/images")
async def get_image(username: str, session: AsyncSession =  Depends(get_session)):
    await get_user_by_username(session, username)
    images: Image = await get_image_by_username(session, username)
    return images


# image router with get request, which returns all images
@router.post("/post_image")
async def post_image(payload: ImageCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await create_image(payload, token, session)


@router.get("/profile/images")
async def get_my_images(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    images: Image = await get_my_image(session, token)
    return images


@router.delete("/profile/image")
async def delete_image( id: int, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await delete_my_image(session, id, token)


@router.patch("/profile/image/edit_name")
async def update_name(id: int, name: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_image_name(session, id, name, token)


@router.patch("/profile/image/edit_image")
async def upgrade_image(id: int, image: str, session: AsyncSession = Depends(get_session), token = Depends(oauth2_scheme)):
    return await edit_image_image(session, id, image, token)
