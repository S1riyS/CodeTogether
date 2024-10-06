from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import PositionModel, ProjectModel, UserModel
from models.associations.application import ApplicationModel, ApplicationStatus
from repositories._base import BaseRepository
from schemas.position import PositionCreateSchema, PositionUpdateSchema


class PositionRepository(BaseRepository[PositionModel, PositionCreateSchema, PositionUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PositionModel)

    async def get_by_project_id(self, project_id: UUID) -> Sequence[PositionModel]:
        """
        Retrieves a sequence of PositionModel instances associated with the given project ID.

        :param project_id: The ID of the project to retrieve positions for.
        :return: A sequence of PositionModel instances.
        """
        statement = select(PositionModel).filter_by(project_id=project_id)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def get_project_owner(self, id_: UUID) -> Optional[UserModel]:
        """
        Get the owner of the project associated with the given position ID.

        :param id_: ID of position
        :return: UserModel of owner if it exists
        """
        result = await self._session.execute(
            select(PositionModel)
            .filter_by(id=id_)
            .options(joinedload(PositionModel.project).joinedload(ProjectModel.owner))
        )
        position = result.scalars().first()
        return position.project.owner if position else None

    async def check_if_user_alerady_applied(self, id_: UUID, user_id: UUID) -> bool:
        """
        Check if the user has already applied for the position.

        :param id_: ID of position
        :param user_id: ID of user
        :return: True if user has already applied for the position, False otherwise
        """
        result = await self._session.execute(select(ApplicationModel).filter_by(position_id=id_, user_id=user_id))
        application = result.scalars().first()
        return application is not None

    async def get_count_of_applications_with_status(self, id_: UUID, application_status: ApplicationStatus) -> int:
        """
        Get the number of approved applications for the position.

        :param id_: ID of position
        :return: Number of approved applications
        """
        count = await self._session.execute(
            select(func.count()).select_from(ApplicationModel).filter_by(position_id=id_, status=application_status)
        )
        return count.scalar_one()
