from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.associations.application import ApplicationModel, ApplicationStatus
from models.position import PositionModel
from models.user import UserModel
from repositories.application_repository import ApplicationRepository
from schemas.application import ApplicationCreateSchema
from services.application_service import ApplicationService
from tests.utils.position import create_new_position
from tests.utils.random_ import random_lower_string
from tests.utils.user import create_new_user


async def create_new_application(
    session: AsyncSession,
    position: Optional[PositionModel] = None,
    user: Optional[UserModel] = None,
) -> ApplicationModel:
    if not position:
        position = await create_new_position(session)
    if not user:
        user = await create_new_user(session)

    application_service = ApplicationService(session)
    return await application_service.create(
        position_id=position.id,
        data=ApplicationCreateSchema(message=random_lower_string()),
        user_id=str(user.id),
    )


async def set_status(session: AsyncSession, application: ApplicationModel, new_status: ApplicationStatus):
    repository = ApplicationRepository(session)
    return await repository.update(application.id, {"status": new_status})
