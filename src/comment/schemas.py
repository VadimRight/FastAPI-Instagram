from pydantic import UUID4, BaseModel


class CommentShema(BaseModel):
    id: UUID4
    text: str
    user_id: str
    post_id: str

class CommentCreate(BaseModel):
    text: str