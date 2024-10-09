from typing import Dict, Optional

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserModel
from schemas.user import UserCreateSchema
from services.user_service import UserService
from tests.utils.random_ import random_email, random_lower_string

__email_password_mapping: Dict[str, str] = {}


async def create_new_user(session: AsyncSession, email: Optional[str] = None) -> UserModel:
    """
    Create a new user in the database.

    If `email` is provided, the created user will have this email. Otherwise, a random one is generated.
    The generated password and username are random.

    The password of the created user is stored in the internal mapping `__email_password_mapping`.
    """
    if not email:
        email = random_email()
    password = random_lower_string()
    username = random_lower_string()

    __email_password_mapping[email] = password

    user_service = UserService(session)
    user_in = UserCreateSchema(email=email, password=password, username=username)
    return await user_service.create(user_in)


async def user_authentication_headers(async_client: AsyncClient, email: str, password: str) -> Dict[str, str]:
    
    """
    Get authentication headers for a user with the given email and password.

    :param async_client: The test client
    :param email: The email of the user to get the authentication headers for
    :param password: The password of the user to get the authentication headers for
    :return: The authentication headers
    """
    credentials = {"username": email, "password": password}
    response = await async_client.post(f"/api/v1/auth/login", data=credentials)

    content = response.json()
    auth_token = content["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_email(
    async_client: AsyncClient, session: AsyncSession, email: str
) -> Dict[str, str]:
    """
    Get authentication headers for a user with the given email.

    If the user does not exist yet, a new one is created with a random username and password.

    :param async_client: The test client
    :param session: The database session
    :param email: The email of the user to get the authentication headers for
    :return: The authentication headers
    """
    user_service = UserService(session)
    user = await user_service.get_by_email(email)

    if not user:
        await create_new_user(session=session, email=email)

    password = __email_password_mapping[email]

    return await user_authentication_headers(async_client=async_client, email=email, password=password)
