from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        from_attributes = True