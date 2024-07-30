from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
