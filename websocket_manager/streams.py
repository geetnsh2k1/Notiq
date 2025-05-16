import logging
import time
import asyncio
from typing import Any, Dict, List, Tuple
from fastapi import status

from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.app_exception import AppException
from redis_client.client import get_redis_client
from config.client import ConfigClient
from utils.helpers import get_group_name, get_stream_key

# Load constants from config; fallback to defaults if not set.
GROUP_NAME: str = get_group_name()
MAX_STREAM_LENGTH: int = int(ConfigClient.get_property("MAX_STREAM_LENGTH", section="WEBSOCKET"))
XREAD_TIMEOUT: int = int(ConfigClient.get_property("XREAD_TIMEOUT", section="WEBSOCKET"))
XREAD_COUNT: int = int(ConfigClient.get_property("XREAD_COUNT", section="WEBSOCKET"))
ERROR_SLEEP_SEC: float = float(ConfigClient.get_property("ERROR_SLEEP_SEC", section="WEBSOCKET"))

logger = logging.getLogger(__name__)
redis_client = get_redis_client()


async def publish_message(user_id: str, message: str) -> None:
    """
    Publish a notification by writing it to a Redis Stream for the given user.
    """
    stream_key: str = get_stream_key(user_id)
    payload: Dict[str, Any] = {"message": message, "timestamp": str(time.time())}
    try:
        msg_id = await redis_client.xadd(
            stream_key,
            payload,
            maxlen=MAX_STREAM_LENGTH,
            approximate=True
        )
        logger.info(
            "[Redis Publisher] Added message to %s: %s (id: %s)",
            stream_key, payload, msg_id
        )
    except Exception as exc:
        logger.error("Error adding message to stream %s: %s", stream_key, exc)


async def create_consumer_group(user_id: str) -> None:
    """
    Ensure that a consumer group exists for a user's notifications stream.
    """
    stream_key: str = get_stream_key(user_id)
    try:
        await redis_client.xgroup_create(
            stream_key, GROUP_NAME, id="0-0", mkstream=True
        )
        logger.info("Created consumer group on stream %s", stream_key)
    except Exception as exc:
        # Ignore BUSYGROUP error indicating the group already exists.
        if "BUSYGROUP" in str(exc):
            logger.debug("Consumer group already exists for stream %s", stream_key)
        else:
            logger.error("Error creating consumer group on stream %s: %s", stream_key, exc)


async def get_pending_notifications(user_id: str) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Retrieve pending notifications from a user's Redis stream using the consumer group.
    Returns a list of (message_id, data) tuples.
    """
    stream_key: str = get_stream_key(user_id)
    consumer_name = user_id  # Using user_id as the consumer identifier.
    notifications: List[Tuple[str, Dict[str, Any]]] = []
    try:
        pending_resp = await redis_client.xreadgroup(
            GROUP_NAME,
            consumer_name,
            {stream_key: "0"},
            count=100,
            block=0
        )
        if pending_resp:
            for _stream, messages in pending_resp:
                notifications.extend(messages)
    except Exception as exc:
        logger.error("Error reading pending notifications from %s: %s", stream_key, exc)
    return notifications


async def listen_for_notifications(user_id: str, websocket) -> None:
    """
    Continuously listen for new notifications from the user's Redis stream and deliver them.
    Uses a blocking XREADGROUP call with a timeout. On errors, sleeps briefly to prevent tight loops.
    """
    stream_key: str = get_stream_key(user_id)
    consumer_name = user_id

    while True:
        try:
            new_resp = await redis_client.xreadgroup(
                GROUP_NAME,
                consumer_name,
                {stream_key: ">"},
                count=XREAD_COUNT,
                block=XREAD_TIMEOUT
            )
            if new_resp:
                for _stream, messages in new_resp:
                    for msg_id, data in messages:
                        message = data.get("message")
                        if message:
                            # Send a JSON payload with both message id and content.
                            await websocket.send_json({"message_id": msg_id, "message": message})
                        # Do not automatically acknowledge the message here;
                        # acknowledgement must be performed explicitly via the new endpoint.
            else:
                # Optional: Sleep briefly between reads if desired.
                await asyncio.sleep(ERROR_SLEEP_SEC)
        except Exception as exc:
            logger.error("Error listening for notifications on stream %s: %s", stream_key, exc)
            await asyncio.sleep(ERROR_SLEEP_SEC)


async def acknowledge_notifications(user_id: str, message_ids: List[str]) -> None:
    """
    Acknowledge (XACK) messages so that they are not redelivered.
    """
    stream_key: str = get_stream_key(user_id)
    try:
        if message_ids:
            await redis_client.xack(stream_key, GROUP_NAME, *message_ids)
    except Exception as exc:
        logger.error("Error acknowledging messages on stream %s: %s", stream_key, exc)
        raise AppException(
            error_code=ErrorCodes.Notification.ACKNOWLEDGE_FAILED,
            error_message=ErrorMessages.Notification.ACKNOWLEDGE_FAILED,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(exc)
        )
