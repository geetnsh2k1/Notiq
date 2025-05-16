from functools import lru_cache
from pydantic_settings import BaseSettings
from config.client import ConfigClient


class RedisSettings(BaseSettings):
    REDIS_HOST: str = ConfigClient.get_property(key="HOST", section="REDIS")
    REDIS_PORT: int = ConfigClient.get_property(key="PORT", section="REDIS")
    REDIS_DB: int = ConfigClient.get_property(key="DB", section="REDIS")

    def get_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache()
def get_redis_settings() -> RedisSettings:
    return RedisSettings()
