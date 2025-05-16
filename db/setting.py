from functools import lru_cache
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings
from typing import Optional
import logging

from config.client import ConfigClient
from utils.aws_secrets_manager import get_secret

logger = logging.getLogger(__name__)


class DBSettings(BaseSettings):
    DB_HOST: str = Field(default_factory=lambda: ConfigClient.get_property("HOST", section="DATABASE"))
    DB_PORT: int = Field(default_factory=lambda: int(ConfigClient.get_property("PORT", section="DATABASE")))
    DB_NAME: str = Field(default_factory=lambda: ConfigClient.get_property("DB_NAME", section="DATABASE"))
    
    DB_USER: str
    DB_PASS: str
    
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    DATABASE_URL: Optional[PostgresDsn] = None

    @classmethod
    def load(cls) -> "DBSettings":
        # Otherwise, fetch secret credentials from AWS Secrets Manager.
        secret_name = ConfigClient.get_property("DB_SECRET_NAME", section="AWS")
        secret_data = get_secret(secret_name)

        username = secret_data.get("username")
        password = secret_data.get("password")

        if not username or not password:
            raise ValueError("Invalid DB credentials in AWS secret")

        return cls(DB_USER=username, DB_PASS=password)

    def get_db_url(self) -> str:
        return (
            self.DATABASE_URL or
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    def get_db_url_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache()
def get_db_settings() -> DBSettings:
    return DBSettings.load()
