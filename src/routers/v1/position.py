from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import CurrentUserDep, SessionDep
from schemas.position import PositionUpdateSchema, PositionSchema
from services.position_service import PositionService

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.put("/{position_id}", response_model=PositionSchema)
async def update_position(position_id: UUID, data: PositionUpdateSchema, user: CurrentUserDep, session: SessionDep):
    position_service = PositionService(session)
    db_obj = await position_service.update(position_id, data, user.id)
    return PositionSchema.from_orm(db_obj)


@router.delete("/{position_id}", response_model=bool)
async def delete_position(position_id: UUID, user: CurrentUserDep, session: SessionDep):
    position_service = PositionService(session)
    result = await position_service.delete(position_id, user.id)
    return result


@router.post("/{position_id}/applications")
async def apply_for_position(position_id: UUID):
    ...


@router.get("/{position_id}/applications")
async def get_applications(position_id: UUID):
    ...
