from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.current_user import get_current_user
from core.database import get_async_session
from models import UserModel

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
