from pydantic import BaseModel


class ImageCreate(BaseModel):
    image: str


class ImageSchema(BaseModel):
    id: int
    image: str
    user_id: int
    class Config:
        from_attributes = True