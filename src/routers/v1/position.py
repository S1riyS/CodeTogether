from uuid import UUID

from fastapi import APIRouter

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.put("/{position_id}")
async def update_position(position_id: UUID):
    ...


@router.delete("/{position_id}")
async def delete_position(position_id: UUID):
    ...


@router.post("/{position_id}/applications")
async def apply_for_position(position_id: UUID):
    ...


@router.get("/{position_id}/applications")
async def get_applications(position_id: UUID):
    ...
