from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    image: bytes
    user_id: int


class ImageCreate(BaseModel):
    image: bytes
    