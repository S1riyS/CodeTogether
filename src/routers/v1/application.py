from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import CurrentUserDep, SessionDep
from schemas import DeleteResponseSchema
from schemas.application import ApplicationSchema, ApplicationUpdateSchema
from services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.put("/{application_id}", response_model=ApplicationSchema)
async def update_application(
    application_id: UUID, data: ApplicationUpdateSchema, user: CurrentUserDep, session: SessionDep
):
    application_service = ApplicationService(session)
    db_obj = await application_service.update(application_id, data, user.id)
    return db_obj


@router.delete("/{application_id}", response_model=DeleteResponseSchema)
async def delete_application(application_id: UUID, user: CurrentUserDep, session: SessionDep):
    application_service = ApplicationService(session)
    result = await application_service.delete(application_id, user.id)
    return DeleteResponseSchema(success=result)


@router.post("/{application_id}/approved", response_model=ApplicationSchema)
async def approve_application(application_id: UUID, user: CurrentUserDep, session: SessionDep):
    application_service = ApplicationService(session)
    db_obj = await application_service.approve(application_id, user.id)
    return db_obj


@router.post("/{application_id}/rejected", response_model=ApplicationSchema)
async def reject_application(application_id: UUID, user: CurrentUserDep, session: SessionDep):
    application_service = ApplicationService(session)
    db_obj = await application_service.reject(application_id, user.id)
    return db_obj
