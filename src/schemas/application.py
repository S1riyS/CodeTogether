from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from models.associations.application import ApplicationStatus
from schemas.utils.decorators import pick
from schemas.utils.mixins import IDSchemaMixin, TimeSchemaMixin


class _BaseApplicationSchema(IDSchemaMixin, TimeSchemaMixin, BaseModel):
    user_id: UUID
    position_id: UUID
    message: str = Field(
        examples=["Hello, I have plenty of experience with this framework"], min_length=1, max_length=1023
    )
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)


class ApplicationSchema(_BaseApplicationSchema):
    model_config = ConfigDict(from_attributes=True)


@pick("message")
class ApplicationCreateSchema(_BaseApplicationSchema): ...


@pick("message")
class ApplicationUpdateSchema(_BaseApplicationSchema): ...
