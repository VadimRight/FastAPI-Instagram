from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
