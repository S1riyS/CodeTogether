from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from schemas.utils.decorators import omit
from schemas.utils.mixins import IDSchemaMixin


class _BaseUserSchema(IDSchemaMixin, BaseModel):
    email: EmailStr
    password: str
    username: str = Field(min_length=1, max_length=255)
    avatar_url: Optional[str] = None
    is_verified: bool = False


@omit('password')
class UserSchema(_BaseUserSchema):
    class Config:
        from_attributes = True


@omit('id', 'avatar_url', 'is_verified')
class UserCreateSchema(_BaseUserSchema):
    ...


@omit('id', 'email', 'password', 'is_verified')
class UserUpdateSchema(_BaseUserSchema):
    ...
