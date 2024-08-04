from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth import security
from core.database import get_async_session
from models import UserModel
from typing_ import IDType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def _get_user(session: AsyncSession, id_: IDType) -> Optional[UserModel]:
    """
    Retrieve a user from the database by their username.

    Args:
        session (AsyncSession): The database session.
        id_ (IDType): The id of the user to retrieve.

    Returns:
        User: The user object if found, otherwise None.
    """
    obj = await session.get(UserModel, id_)
    return obj


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    """
    Get the current user based on the provided token.

    Args:
        token (str): The authentication token.
        session (Session): The database session.

    Raises:
        HTTPException: If credentials cannot be validated.

    Returns:
        User: The current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: IDType = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await _get_user(session, id_=user_id)
    if user is None:
        raise credentials_exception
    return user
