from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import CurrentUserDep, SessionDep
from schemas.user import UserSchema, UserUpdateSchema
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserSchema)
async def get_me(user: CurrentUserDep):
    return user


@router.put("/me", response_model=UserSchema)
async def update_user(user: CurrentUserDep, data: UserUpdateSchema, session: SessionDep):
    user_service = UserService(session)
    return await user_service.update(user.id, data)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: UUID, session: SessionDep):
    user_service = UserService(session)
    return await user_service.get_by_id(user_id)
