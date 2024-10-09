from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.associations.application import ApplicationModel, ApplicationStatus
from repositories.application_repository import ApplicationRepository
from schemas.application import ApplicationCreateSchema, ApplicationUpdateSchema
from services.position_service import PositionService


class ApplicationService:
    def __init__(self, session: AsyncSession):
        self._repository = ApplicationRepository(session)
        self._position_service = PositionService(session)

    async def create(self, position_id: UUID, data: ApplicationCreateSchema, user_id: UUID) -> ApplicationModel:
        position = await self._position_service.get_by_id(position_id)

        owner = await self._position_service.get_project_owner(position.id)
        if owner.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The owner cannot apply for positions in his project",
            )

        if await self._position_service.check_if_user_alerady_applied(position.id, user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this position",
            )

        approved_applcications_count = await self._position_service.get_count_of_applications_with_status(
            position_id, ApplicationStatus.APPROVED
        )
        if approved_applcications_count >= position.count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are no vacant slots for this position",
            )

        new_application = await self._repository.create(data, position_id=position_id, user_id=user_id)
        if new_application is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating an application",
            )
        return new_application

    async def _get_by_id(self, application_id: UUID) -> ApplicationModel:
        application = await self._repository.get_by_id(application_id)
        if application is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        return application

    async def get_all_by_position_id(self, position_id: UUID, user_id: UUID) -> Sequence[ApplicationModel]:
        position = await self._position_service.get_by_id(position_id)
        owner = await self._position_service.get_project_owner(position.id)
        if owner.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return await self._repository.get_all_by_position_id(position_id)

    async def update(self, application_id: UUID, data: ApplicationUpdateSchema, user_id: UUID):
        application = await self._get_by_id(application_id)
        if application.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        updated_application = await self._repository.update(application_id, data)
        if updated_application is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while updating an application",
            )
        return updated_application

    async def delete(self, application_id: UUID, user_id: UUID) -> bool:
        application = await self._get_by_id(application_id)
        if application.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return await self._repository.delete(application_id)

    async def __set_status(
        self, application_id: UUID, new_status: ApplicationStatus, user_id: UUID
    ) -> ApplicationModel:
        """
        Sets the status of an application.

        :param application_id: The ID of the application to update.
        :param new_status: The new status of the application.
        :param user_id: The ID of the user updating the application status.
        :return: None
        """
        application = await self._get_by_id(application_id)

        if application.status != ApplicationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Status change is allowed only for "PENDING" applications',
            )

        position = await self._position_service.get_by_id(application.position_id)
        owner = await self._position_service.get_project_owner(position.id)
        if owner.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        updated_application = await self._repository.update(application_id, {"status": new_status})
        if updated_application is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while updating status",
            )

        return updated_application

    async def approve(self, application_id: UUID, user_id: UUID) -> ApplicationModel:
        application = await self._get_by_id(application_id)
        position = await self._position_service.get_by_id(application.position_id)

        approved_applcications_count = await self._position_service.get_count_of_applications_with_status(
            position.id, ApplicationStatus.APPROVED
        )

        if approved_applcications_count >= position.count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are no vacant slots for this position",
            )

        return await self.__set_status(application_id, ApplicationStatus.APPROVED, user_id)

    async def reject(self, application_id: UUID, user_id: UUID) -> ApplicationModel:
        return await self.__set_status(application_id, ApplicationStatus.REJECTED, user_id)
