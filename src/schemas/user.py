from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from schemas.utils.decorators import omit, pick
from schemas.utils.mixins import IDSchemaMixin


class _BaseUserSchema(IDSchemaMixin, BaseModel):
    email: EmailStr
    password: str
    username: str = Field(min_length=1, max_length=255)
    avatar_url: Optional[str] = None
    is_verified: bool = False


@omit("password")
class UserSchema(_BaseUserSchema):
    class Config:
        from_attributes = True


@pick("email", "username", "password")
class UserCreateSchema(_BaseUserSchema): ...


@pick("email", "username")
class UserUpdateSchema(_BaseUserSchema): ...
