from pydantic import UUID4, BaseModel


class LikeCommentSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    post_id: UUID4