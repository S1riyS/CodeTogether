from uuid import UUID

from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.put("/{application_id}")
async def update_application(position_id: UUID, application_id: UUID):
    ...


@router.delete("/{application_id}")
async def delete_application(position_id: UUID, application_id: UUID):
    ...


@router.post("/{application_id}/approved")
async def approve_application(position_id: UUID, application_id: UUID):
    ...


@router.post("/{application_id}/rejected")
async def reject_application(position_id: UUID, application_id: UUID):
    ...

