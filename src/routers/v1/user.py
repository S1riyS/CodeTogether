from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import SessionDep
from schemas.user import UserSchema
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserSchema)
async def get_users(user_id: UUID, session: SessionDep):
    user_service = UserService(session)
    db_obj = await user_service.get_by_id(user_id)
    return UserSchema.from_orm(db_obj)
