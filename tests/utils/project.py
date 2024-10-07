from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserModel
from schemas.project import ProjectCreateSchema
from services.project_service import ProjectService
from tests.utils.user import create_new_user


async def create_new_project(session: AsyncSession, owner: Optional[UserModel] = None):
    if not owner:
        owner = await create_new_user(session)

    project_service = ProjectService(session)
    return await project_service.create(
        ProjectCreateSchema(
            name="Test Project",
            description="Description of project",
            difficulty="easy",
            owner_id=str(owner.id),
        ),
        str(owner.id),
    )
