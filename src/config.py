from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_name: str = Field("code_together", env="DB_NAME")
    db_user: str = Field("postgres", env="DB_USER")
    db_pass: str = Field("root", env="DB_PASS")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class AuthSettings(BaseSettings):
    secret_key: str = Field("super_secret_key", env="SECRET")
    algorithm: str = Field("HS256", env="HASH_ALGORITHM")
    access_token_expire_minutes: int = Field(30, env='ACCESS_TOKEN_EXPIRE_MINUTES')


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
