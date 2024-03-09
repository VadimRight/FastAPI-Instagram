from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    image: str
    user_id: int


class ImageCreate(BaseModel):
    image: str
