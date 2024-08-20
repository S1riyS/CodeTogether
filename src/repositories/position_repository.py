from typing import List, Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import PositionModel, UserModel, ProjectModel
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

    async def get_project_owner(self, id_: IDType) -> Optional[UserModel]:
        result = await self._session.execute(
            select(PositionModel)
            .filter_by(id=id_)
            .options(
                joinedload(PositionModel.project).
                joinedload(ProjectModel.owner)
            )
        )
        position = result.scalars().first()
        return position.project.owner if position else None
