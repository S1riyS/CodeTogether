from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.utils.decorators import omit
from schemas.utils.mixins import IDSchemaMixin


class _BasePositionSchema(IDSchemaMixin, BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str]
    count: int = Field(default=1, ge=1)
    project_id: UUID


@omit('project_id')
class PositionSchema(_BasePositionSchema):
    class Config:
        from_attributes = True


@omit('id', 'project_id')
class PositionCreateSchema(_BasePositionSchema):
    ...


@omit('id', 'project_id')
class PositionUpdateSchema(_BasePositionSchema):
    ...
