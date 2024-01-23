from fastapi import APIRouter


image_router = APIRouter(

)


@image_router("/")
async def image_endpoint():
    pass