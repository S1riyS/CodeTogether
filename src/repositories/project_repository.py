from sqlalchemy.ext.asyncio import AsyncSession

from models import ProjectModel
from repositories._base import BaseRepository
from schemas.project import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository(BaseRepository[ProjectModel, ProjectCreateSchema, ProjectUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectModel)
    