from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from models import ApplicationModel
from models.associations.application import ApplicationStatus
from repositories._base import BaseRepository
from schemas.application import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationRepository(BaseRepository[ApplicationModel, ApplicationCreateSchema, ApplicationUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ApplicationModel)

    async def get_all_by_position_id(self, position_id: UUID) -> Sequence[ApplicationModel]:
        """
        Retrieves all applications associated with the given position ID.

        :param position_id: The ID of the position to retrieve applications for.
        :return: A sequence of ApplicationModel instances.
        """
        statement = select(ApplicationModel).filter_by(position_id=position_id)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def get_all_by_position_id_and_status(
        self, position_id: UUID, status: ApplicationStatus
    ) -> Sequence[ApplicationModel]:
        """
        Retrieves all applications associated with the given position ID and status.

        :param position_id: The ID of the position to retrieve applications for.
        :param status: The status of the applications to retrieve.
        :return: A sequence of ApplicationModel instances.
        """
        statement = select(ApplicationModel).filter_by(position_id=position_id, status=status)
        result = await self._session.execute(statement)
        return result.scalars().all()
