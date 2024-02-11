from pydantic import BaseModel, Field, EmailStr


# Schema for getting user and superclass for other schemas
class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str


# Schema for user registration
class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


#  Schema for getting User with all rows
class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = True
    is_verified: bool = False

    class Config:
        from_attributes = True


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for storing in token username
class TokenData(BaseModel):
    username: str | None = None


# Schema for user auth by token
class UserInDB(UserSchema):
    hashed_password: str
