from typing import List
from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import CurrentUserDep, SessionDep
from schemas.application import ApplicationCreateSchema, ApplicationSchema
from schemas.position import PositionSchema, PositionUpdateSchema
from services.application_service import ApplicationService
from services.position_service import PositionService

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.put("/{position_id}", response_model=PositionSchema)
async def update_position(
    position_id: UUID,
    data: PositionUpdateSchema,
    user: CurrentUserDep,
    session: SessionDep,
):
    position_service = PositionService(session)
    db_obj = await position_service.update(position_id, data, user.id)
    return PositionSchema.from_orm(db_obj)


@router.delete("/{position_id}", response_model=bool)
async def delete_position(position_id: UUID, user: CurrentUserDep, session: SessionDep):
    position_service = PositionService(session)
    result = await position_service.delete(position_id, user.id)
    return result


@router.post("/{position_id}/applications", response_model=ApplicationSchema)
async def apply_for_position(
    position_id: UUID,
    data: ApplicationCreateSchema,
    user: CurrentUserDep,
    session: SessionDep,
):
    application_service = ApplicationService(session)
    db_obj = await application_service.create(position_id, data, user.id)
    return ApplicationSchema.from_orm(db_obj)


@router.get("/{position_id}/applications", response_model=List[ApplicationSchema])
async def get_applications(position_id: UUID, user: CurrentUserDep, session: SessionDep):
    application_service = ApplicationService(session)
    db_list = await application_service.get_all_by_position_id(position_id, user.id)
    return [ApplicationSchema.from_orm(application) for application in db_list]
