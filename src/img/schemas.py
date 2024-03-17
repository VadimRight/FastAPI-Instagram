from pydantic import BaseModel

# Pydantic schema for get image request

class ImageCreate(BaseModel):
    image: str
    name: str

class ImageSchema(BaseModel):
    id: int
    image: str
    user_id: int
    name: str

    class Config:
        from_attributes = True


class ShowImage(ImageCreate):
    name: str
