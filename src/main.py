from fastapi import FastAPI

from src.img.router import router as image_router
from src.auth.router import router as user_router

# FastAPI App initialization
app = FastAPI(
    title='Image Editor'
)

# Image and User Routers are included in app
app.include_router(image_router)
app.include_router(user_router)
