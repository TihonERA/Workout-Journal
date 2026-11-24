from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(default=...)
    POSTGRES_PORT: int = Field(default=...)
    POSTGRES_USER: str = Field(default=...)
    POSTGRES_PASS: str = Field(default=...)
    POSTGRES_NAME: str = Field(default=...)

    @computed_field
    @property
    def DATABASE_URL_asyncpg(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASS,
            path=self.POSTGRES_NAME,
        )

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
