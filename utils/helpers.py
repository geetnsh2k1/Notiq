import os
from config.client import ConfigClient


def get_stream_key(user_id: str) -> str:
    env = os.getenv("APP_ENV", "local")
    app = ConfigClient.get_property("APP_NAME").lower()
    stream_prefix = ConfigClient.get_property("REDIS_STREAM_PREFIX", section="WEBSOCKET")
    return f"{env}:{app}:{stream_prefix}:{user_id}"

def get_group_name() -> str:
    env = os.getenv("APP_ENV", "local")
    app = ConfigClient.get_property("APP_NAME").lower()
    group_prefix = ConfigClient.get_property("GROUP_NAME", section="WEBSOCKET")
    return f"{env}:{app}:{group_prefix}"