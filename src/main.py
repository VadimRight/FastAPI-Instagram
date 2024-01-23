from fastapi import FastAPI
from src.router import router
app = FastAPI(
    title='Image Editor'
)
app.include_router(router)

