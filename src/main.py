from fastapi import FastAPI

from src.post.router import router as image_router
from src.auth.router import router as user_router
from src.comment.router import router as comment_router

# FastAPI App initialization
app = FastAPI(
    title='Instagram FastAPI'
)

# Post and User Routers are included in app
app.include_router(image_router)
app.include_router(user_router)
app.include_router(comment_router)