from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False

    class Config:
        from_attributes = True