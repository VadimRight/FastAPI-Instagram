from pydantic import BaseModel


class CommentShema(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int

class CommentCreate(BaseModel):
    text: str