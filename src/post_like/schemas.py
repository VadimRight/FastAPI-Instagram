from pydantic import UUID4, BaseModel


class LikeSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    post_id: UUID4

    class Config:
        from_attributes = True
