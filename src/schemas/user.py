from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

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
    model_config = ConfigDict(from_attributes=True)


@pick("email", "username", "password")
class UserCreateSchema(_BaseUserSchema): ...


@pick("username")
class UserUpdateSchema(_BaseUserSchema): ...
