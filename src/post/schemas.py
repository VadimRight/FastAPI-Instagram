from pydantic import UUID4, BaseModel

# Pydantic schema for get image request

class PostCreate(BaseModel):
    text: str
    name: str

class PostSchema(BaseModel):
    id: UUID4
    text: str
    user_id: UUID4
    name: str
    class Config:
        from_attributes = True


class ShowPost(PostCreate):
    name: str
