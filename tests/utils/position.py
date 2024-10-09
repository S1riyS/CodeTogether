from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.position import PositionModel
from models.project import ProjectModel
from schemas.position import PositionCreateSchema
from services.position_service import PositionService
from tests.utils.project import create_new_project
from tests.utils.random_ import random_lower_string


async def create_new_position(
    session: AsyncSession,
    project: Optional[ProjectModel] = None,
    count: int = 1,
) -> PositionModel:
    if not project:
        project = await create_new_project(session)

    position_service = PositionService(session)
    return await position_service.create(
        project_id=project.id,
        data=PositionCreateSchema(
            name=f"Position {random_lower_string()}",
            description="Description of position",
            count=count,
        ),
        user_id=str(project.owner_id),
    )
