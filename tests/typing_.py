from pydantic import BaseModel, ConfigDict, EmailStr


class UserCredentials(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str
    username: str
