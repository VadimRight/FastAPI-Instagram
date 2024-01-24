import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import get_session, SessionLocal
from src.models.models import Image
from fastapi import FastAPI, Request, Response, status
router = APIRouter()


@router.get("/big_picture")
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("/images")
async def get_image():
    async with SessionLocal() as session:
        q = select(Image)
        result = await session.execute(q)
        curr = result.scalars().all()
        print(curr)
        return {"status": "success", "data": curr, "details": None}


@router.post("/images")
async def post_image(image: str):
    async with SessionLocal() as session:
        stock_image = Image(image=image)
        session.add(stock_image)
        await session.commit()
        return {"image_added": stock_image.image}
