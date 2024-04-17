from pydantic import UUID4, BaseModel, Field, EmailStr
from uuid import UUID

# Schema for getting user and superclass for other schemas
class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str


# Schema for user registration
class CreateUserResponceSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


#  Schema for getting User with all rows
class UserSchema(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserResponceSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
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
    id: UUID4 | None = None

# Schema for user auth by token
class UserInDB(UserResponceSchema):
    id: UUID4
    hashed_password: str
