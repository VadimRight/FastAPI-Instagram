from fastapi import FastAPI

from src.router import router as image_router
from src.auth.router import router as user_router
app = FastAPI(
    title='Image Editor'
)
app.include_router(image_router)
app.include_router(user_router)
