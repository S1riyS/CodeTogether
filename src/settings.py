from pydantic import Field
from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT, ".env")


_default_model_config = SettingsConfigDict(
    env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
)


class PostgresSettings(BaseSettings):
    """Settings for postgres"""

    model_config = _default_model_config

    db_host: str = Field(alias="POSTGRES_HOST")
    db_port: int = Field(alias="POSTGRES_PORT")
    db_name: str = Field(alias="POSTGRES_DB")
    db_user: str = Field(alias="POSTGRES_USER")
    db_pass: str = Field(alias="POSTGRES_PASSWORD")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class AuthSettings(BaseSettings):
    """Settings for auth"""

    model_config = _default_model_config

    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")


class Settings(BaseSettings):
    model_config = _default_model_config

    environment: str = Field(alias="ENVIRONMENT")
    postgres: PostgresSettings = PostgresSettings()
    auth: AuthSettings = AuthSettings()


@lru_cache()
def get_settings() -> Settings:
    """Function for getting all settings."""
    return Settings()


settings = get_settings()
