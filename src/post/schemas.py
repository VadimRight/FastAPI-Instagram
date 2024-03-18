from pydantic import UUID4, BaseModel

# Pydantic schema for get image request

class PostCreate(BaseModel):
    image: str
    name: str

class PostSchema(BaseModel):
    id: UUID4
    image: str
    user_id: str
    name: str

    class Config:
        from_attributes = True


class ShowPost(PostCreate):
    name: str
