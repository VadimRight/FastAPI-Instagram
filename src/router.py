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
async def get_image(image_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Image).where(Image.id == image_id)
    results = await session.execute(query)
    return results.scalars().all()

# @router.post("/images")
# async def post_image(request: Request, responce: Response, image: Image):
#     try:
#         SessionLocal.begin()
#         image_record = Image(**dict(image))
#         SessionLocal.add(image_record)
#         SessionLocal.commit()
#         image.id = image_record.id
#         return image
#     except Exception as e:
#         SessionLocal.rollback()
#         responce.status_code = status.HTTP_404_NOT_FOUND
#         return {
#             "error": e,
#             "error_details": e.orig.args if hasattr(e, "orig") else f"{e}"
#         }

