from uuid import UUID

from pydantic import BaseModel, Field

from models.project import Difficulty
from schemas.utils.decorators import omit
from schemas.utils.mixins import IDSchemaMixin, TimeSchemaMixin


class _BaseProjectSchema(IDSchemaMixin, TimeSchemaMixin, BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str
    difficulty: Difficulty
    owner_id: UUID


class ProjectSchema(_BaseProjectSchema):
    class Config:
        from_attributes = True


@omit('id', 'created_at', 'updated_at', 'owner_id')
class ProjectCreateSchema(_BaseProjectSchema):
    ...


@omit('id', 'created_at', 'updated_at', 'owner_id')
class ProjectUpdateSchema(_BaseProjectSchema):
    ...
