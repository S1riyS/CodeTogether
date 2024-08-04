from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import UserModel
from repositories.user_repository import UserRepository
from schemas.user import UserCreateSchema, UserUpdateSchema
from services.utils.repository_validation import validate_creation, validate_update
from typing_ import IDType


class UserService:
    def __init__(self, session: AsyncSession):
        self._repository = UserRepository(session)

    async def create(self, data: UserCreateSchema) -> UserModel:
        if await self._repository.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if await self._repository.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

        new_user = await self._repository.create(data)
        validate_creation(new_user)
        return new_user

    async def get_by_id(self, id_: IDType) -> UserModel:
        user = await self._repository.get_by_id(id_)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_by_email(self, email: str) -> UserModel:
        user = await self._repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update(self, id_: IDType, data: UserUpdateSchema) -> UserModel:
        if not await self._repository.exists_by_id(id_):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        updated_user = await self._repository.update(id_, data)
        validate_update(updated_user)
        return updated_user

    async def delete(self, id_: IDType) -> bool:
        if not await self._repository.exists_by_id(id_):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return await self._repository.delete(id_)
