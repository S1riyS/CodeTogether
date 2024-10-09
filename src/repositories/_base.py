from abc import ABC
from typing import Any, Dict, Generic, Optional, Type, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from typing_ import CreateSchemaType, ModelType, UpdateSchemaType


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._session = session
        self._model = model

    async def get_by_id(self, id_: UUID) -> Optional[ModelType]:
        obj = await self._session.get(self._model, id_)
        return obj

    async def exists_by_id(self, id_: UUID) -> bool:
        obj = await self.get_by_id(id_)
        return obj is not None

    async def create(self, obj: CreateSchemaType, **kwargs) -> Optional[ModelType]:
        db_obj: ModelType = self._model(**obj.model_dump(), **kwargs)
        self._session.add(db_obj)

        try:
            await self._session.commit()
            return db_obj
        except IntegrityError:
            await self._session.rollback()
            return None

    async def update(self, id_: UUID, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        db_obj = await self.get_by_id(id_)
        # Check if exists
        if db_obj:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            # Update the object
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            await self._session.flush()
            await self._session.refresh(db_obj)

            await self._session.commit()

        return db_obj

    async def delete(self, id_: UUID) -> bool:
        try:
            db_obj = await self._session.get(self._model, id_)
            await self._session.delete(db_obj)
            await self._session.commit()
            return True
        except DatabaseError:
            await self._session.rollback()
            return False
