from abc import ABC
from typing import Generic, Type, Optional

from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from typing_ import ModelType, CreateSchemaType, UpdateSchemaType, IDType


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._session = session
        self._model = model

    async def get_by_id(self, id_: IDType) -> Optional[ModelType]:
        obj = await self._session.get(self._model, id_)
        return obj

    async def exists_by_id(self, id_: IDType) -> bool:
        obj = await self.get_by_id(id_)
        return obj is not None

    async def create(self, obj: CreateSchemaType, **kwargs) -> Optional[ModelType]:
        db_obj: ModelType = self._model(**obj.dict(), **kwargs)
        self._session.add(db_obj)

        try:
            await self._session.commit()
            return db_obj
        except IntegrityError:
            await self._session.rollback()
            return None

    async def update(self, id_: IDType, obj: UpdateSchemaType) -> Optional[ModelType]:
        try:
            db_obj = await self.get_by_id(id_)
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            await self._session.commit()
            return db_obj
        except DatabaseError:
            await self._session.rollback()
            return None

    async def delete(self, id_: IDType) -> bool:
        try:
            db_obj = await self._session.get(self._model, id_)
            await self._session.delete(db_obj)
            await self._session.commit()
            return True
        except DatabaseError:
            await self._session.rollback()
            return False
