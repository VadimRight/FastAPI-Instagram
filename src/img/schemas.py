from pydantic import BaseModel

# Pydantic schema for get image request
class ImageSchema(BaseModel):
    id: int
    image: str
    user_id: int


# Pydantic schema for post request for image
class ImageCreate(BaseModel):
    image: str
