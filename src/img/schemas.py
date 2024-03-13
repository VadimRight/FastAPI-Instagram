from pydantic import BaseModel

# Pydantic schema for get image request

class ImageCreate(BaseModel):
    image: str


class ImageSchema(BaseModel):
    id: int
    image: str
    user_id: int
    class Config:
        from_attributes = True


class ShowImage(ImageCreate):
    username: str
