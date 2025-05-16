from redis import asyncio as aioredis

from redis_client.setting import get_redis_settings

redis_settings = get_redis_settings()

redis_client: aioredis.Redis = aioredis.from_url(
    redis_settings.get_redis_url(),
    decode_responses=True,
)

# dependencies.py
def get_redis_client() -> aioredis.Redis:
    return redis_client
