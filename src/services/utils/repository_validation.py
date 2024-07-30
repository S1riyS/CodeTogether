from fastapi import HTTPException
from starlette import status

from core.database import Base


def validate_creation(created_obj: Base) -> None:
    if created_obj is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating a record")


def validate_update(updated_obj: Base) -> None:
    if updated_obj is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating a record")
