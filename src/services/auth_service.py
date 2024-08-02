from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.security import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models import UserModel
from schemas.auth import TokenSchema
from schemas.user import UserCreateSchema as RegisterSchema

from services.user_service import UserService


class AuthService:
    def __init__(self, session: AsyncSession):
        self._user_service = UserService(session)

    async def signup(self, register_schema: RegisterSchema) -> UserModel:
        return await self._user_service.create(register_schema)

    async def login(self, data: OAuth2PasswordRequestForm) -> TokenSchema:
        invalid_credentials_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        candidate = await self._user_service.get_by_email(data.username)
        if candidate is None:
            raise invalid_credentials_exc
        if not pwd_context.verify(data.password, candidate.hashed_password):
            raise invalid_credentials_exc

        payload = {"sub": str(candidate.id)}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data=payload, expires_delta=access_token_expires)

        return TokenSchema(access_token=access_token, token_type="bearer")
