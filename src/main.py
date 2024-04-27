from fastapi import FastAPI

from src.post.router import router as image_router
from src.auth.router import router as user_router
from src.comment.router import router as comment_router
from contextlib import asynccontextmanager


# FastAPI App initialization
app = FastAPI(
    title='Instagram FastAPI',
)

# Post and User Routers are included in app
app.include_router(image_router)
app.include_router(user_router)
app.include_router(comment_router)

@app.on_event("startup")
async def startup_event():
    with open('./data/data.txt', 'r') as file:
        lines = file.readlines()
    with open('./data/data.txt', 'w') as file:
        for number, line in enumerate(lines):
            if number >= 0:
                file.truncate()


