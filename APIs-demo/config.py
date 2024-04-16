from enum import Enum

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL: PostgresDsn = (
        "postgresql+asyncpg://userb:password@127.0.0.1:5432/db_name"
    )
    JWT_SECRET: str = "lshweow1282034lskdls1nndbci-=+qqwrffxuzbqks"


config: Config = Config()