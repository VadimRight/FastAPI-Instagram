import time

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import get_session, SessionLocal
from src.img.crud import create_image, get_image_by_username
from src.img.schemas import ImageCreate, ShowImage
from src.models.models import Image
from fastapi import FastAPI, Request, Response, status
from src.auth.oauth import oauth2_scheme
router = APIRouter(
    tags=["Image"]
)


# Router for testing connection to database
@router.get("/big_picture")
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


# Router for getting all images
@router.get("/users/{username}/images")
async def get_image(username: str, session: AsyncSession =  Depends(get_session)):
    images: Image = await get_image_by_username(session, username)
    return images

# image router with get request, which returns all images
@router.post("/post_image")
async def post_image(payload: ImageCreate = Body(), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    return await create_image(payload, token, session)