import asyncio
from typing import AsyncGenerator, Dict

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from core.database import get_async_session, metadata
from main import app
from schemas.user import UserCreateSchema
from services.user_service import UserService
from tests.typing_ import UserCredentials
from tests.utils.random_ import random_email, random_lower_string
from tests.utils.user import user_authentication_headers

# Database
DATABASE_URL_TEST = "postgresql+asyncpg://postgres:root@localhost:5432/code_together_test"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="function", autouse=True)
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# Client
@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


# User
@pytest.fixture(scope="session")
def defalt_user_credentials() -> UserCredentials:
    return UserCredentials(
        email=random_email(),
        password=random_lower_string(),
        username=random_lower_string(),
    )


@pytest.fixture(scope="session", autouse=True)
async def create_defalt_user(prepare_database: None, defalt_user_credentials: UserCredentials):
    async with async_session_maker() as session:
        user_service = UserService(session)
        user_in = UserCreateSchema(
            email=defalt_user_credentials.email,
            password=defalt_user_credentials.password,
            username=defalt_user_credentials.username,
        )
        await user_service.create(user_in)


@pytest.fixture(scope="session")
async def default_user_token_headers(
    async_client: AsyncClient, defalt_user_credentials: UserCredentials
) -> Dict[str, str]:
    return await user_authentication_headers(
        async_client=async_client,
        email=defalt_user_credentials.email,
        password=defalt_user_credentials.password,
    )
