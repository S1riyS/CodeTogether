from uuid import UUID

from pydantic import BaseModel, Field

from models.project import Difficulty
from schemas.utils.decorators import omit, pick
from schemas.utils.mixins import IDSchemaMixin, TimeSchemaMixin


class _BaseProjectSchema(IDSchemaMixin, TimeSchemaMixin, BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str
    difficulty: Difficulty
    owner_id: UUID


class ProjectSchema(_BaseProjectSchema):
    class Config:
        from_attributes = True


@pick("name", "description", "difficulty")
class ProjectCreateSchema(_BaseProjectSchema): ...


@pick("name", "description", "difficulty")
class ProjectUpdateSchema(_BaseProjectSchema): ...
