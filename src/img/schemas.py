from pydantic import BaseModel

# Pydantic schema for get image request

class PostCreate(BaseModel):
    image: str
    name: str

class PostSchema(BaseModel):
    id: int
    image: str
    user_id: int
    name: str

    class Config:
        from_attributes = True


class ShowPost(PostCreate):
    name: str
