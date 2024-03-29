from pydantic import UUID4, BaseModel


class LikePostSchema(BaseModel):
    id:  UUID4
    user_id: UUID4
    post_id: UUID4

    class Config(BaseModel):
        from_attributes = True