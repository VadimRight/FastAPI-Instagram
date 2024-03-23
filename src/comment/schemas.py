from pydantic import UUID4, BaseModel


class CommentShema(BaseModel):
    id: UUID4
    text: str
    user_id: UUID4
    post_id: UUID4

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str