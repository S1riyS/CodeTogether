from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import get_password_hash
from models import UserModel
from repositories._base import BaseRepository
from schemas.user import UserCreateSchema, UserUpdateSchema


class UserRepository(BaseRepository[UserModel, UserCreateSchema, UserUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(query)
        obj = result.scalars().one_or_none()
        return obj

    async def exists_by_email(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        query = select(UserModel).where(UserModel.username == username)
        result = await self._session.execute(query)
        obj = result.scalars().one_or_none()
        return obj

    async def exists_by_username(self, email: str) -> bool:
        user = await self.get_by_username(email)
        return user is not None

    async def create(self, obj: UserCreateSchema, **kwargs) -> Optional[UserModel]:
        # Replace password with hashed password
        user_dict = obj.dict()
        password = user_dict.pop("password")

        user_dict["hashed_password"] = get_password_hash(password)

        # Save user to database
        db_obj: UserModel = self._model(**user_dict)
        self._session.add(db_obj)

        # Try to commit changes to database.
        try:
            await self._session.commit()
            return db_obj
        except IntegrityError:
            await self._session.rollback()
            return None
