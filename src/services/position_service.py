from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import PositionModel, UserModel
from models.associations.application import ApplicationStatus
from repositories.position_repository import PositionRepository
from schemas.position import PositionCreateSchema, PositionUpdateSchema
from services.project_service import ProjectService
from typing_ import IDType


class PositionService:
    def __init__(self, session: AsyncSession):
        self._repository = PositionRepository(session)
        self._project_service = ProjectService(session)

    async def create(self, project_id: IDType, data: PositionCreateSchema, user_id: IDType) -> PositionModel:
        await self.__check_project_ownership(project_id, user_id)

        new_position = await self._repository.create(data, project_id=project_id)
        if new_position is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating a position",
            )

        return new_position

    async def get_by_id(self, id_: IDType) -> PositionModel:
        position = await self._repository.get_by_id(id_)
        if position is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")

        return position

    async def get_all_by_project_id(self, project_id: IDType) -> Sequence[PositionModel]:
        return await self._repository.get_by_project_id(project_id)

    async def update(self, id_: IDType, data: PositionUpdateSchema, user_id: IDType):
        position = await self.get_by_id(id_)
        await self.__check_project_ownership(position.project_id, user_id)

        updated_position = await self._repository.update(id_, data)
        if updated_position is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while updating a position",
            )
        return updated_position

    async def delete(self, id_: IDType, user_id: IDType) -> bool:
        position = await self.get_by_id(id_)
        await self.__check_project_ownership(position.project_id, user_id)

        return await self._repository.delete(id_)

    async def get_project_owner(self, id_: IDType) -> UserModel:
        owner = await self._repository.get_project_owner(id_)
        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Owner of project not found",
            )
        return owner

    async def check_if_user_alerady_applied(self, position_id: IDType, user_id: IDType) -> bool:
        return await self._repository.check_if_user_alerady_applied(position_id, user_id)

    async def get_count_of_applications_with_status(self, position_id: IDType, status: ApplicationStatus) -> int:
        return await self._repository.get_count_of_applications_with_status(position_id, status)

    async def __check_project_ownership(self, project_id: IDType, user_id: IDType) -> None:
        """
        Check if the provided user has ownership of the given project.

        :param project_id: The ID of the project.
        :param user_id: The ID of the user.
        :raises HTTPException: If the user does not have ownership.
        """

        project = await self._project_service.get_by_id(project_id)
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")