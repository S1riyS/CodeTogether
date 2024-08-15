from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import ProjectModel
from repositories.project_repository import ProjectRepository
from schemas.project import ProjectCreateSchema, ProjectUpdateSchema
from typing_ import IDType


class ProjectService:
    def __init__(self, session: AsyncSession):
        self._repository = ProjectRepository(session)

    async def create(self, data: ProjectCreateSchema, user_id: IDType) -> ProjectModel:
        new_project = await self._repository.create(data, owner_id=user_id)
        if new_project is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating a project"
            )
        return new_project

    async def get_by_id(self, id_: IDType) -> ProjectModel:
        project = await self._repository.get_by_id(id_)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def update(self, id_: IDType, data: ProjectUpdateSchema, user_id: IDType) -> ProjectModel:
        candidate = await self._repository.get_by_id(id_)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        if candidate.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        updated_project = await self._repository.update(id_, data)
        if updated_project is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while updating a project"
            )
        return updated_project

    async def delete(self, id_: IDType, user_id: IDType) -> bool:
        candidate = await self._repository.get_by_id(id_)

        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if candidate.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return await self._repository.delete(id_)
