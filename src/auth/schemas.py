from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")
    username: str
    email: EmailStr


class UserSchema(UserBaseSchema):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(UserSchema):
    hashed_password: str
