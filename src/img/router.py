import time

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import get_session, SessionLocal
from src.img.crud import create_image
from src.img.schemas import ImageCreate
from src.models.models import Image
from fastapi import FastAPI, Request, Response, status
router = APIRouter(
    tags=["Image"]
)


# Router for testing connection to database
@router.get("/big_picture")
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


# Router for getting all images
@router.get("/images")
async def get_image():
    async with SessionLocal() as session:
        q = select(Image)
        result = await session.execute(q)
        curr = result.scalars().all()
        print(curr)
        return {"status": "success", "data": curr, "details": None}


# image router with get request, which returns all images
@router.post("/post_image")
async def post_image(payload: ImageCreate = Body(),
                     session: AsyncSession = Depends(get_session)):
    return await create_image(payload, session)