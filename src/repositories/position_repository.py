from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import PositionModel
from repositories._base import BaseRepository
from schemas.position import PositionCreateSchema, PositionUpdateSchema
from typing_ import IDType


class PositionRepository(BaseRepository[PositionModel, PositionCreateSchema, PositionUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PositionModel)

    async def get_by_project_id(self, project_id: IDType) -> Sequence[PositionModel]:
        statement = select(PositionModel).filter_by(project_id=project_id)
        result = await self._session.execute(statement)
        return result.scalars().all()
