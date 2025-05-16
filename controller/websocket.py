import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Depends

from constants.endpoints import Endpoints
from websocket_manager.connection_manager import manager
from websocket_manager.streams import (
    publish_message,
    create_consumer_group,
    get_pending_notifications,
    listen_for_notifications,
)
from dependencies.dao import get_client_dao
from repository.client import ClientDAO

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["api"],
)


@router.websocket(
    path=Endpoints.WebSocket.WS_CONNECTION,
    name="WebSocket Connection",
)
async def websocket_endpoint(
    websocket: WebSocket,
    client_name: str,
    user_id: str,
    client_dao: ClientDAO = Depends(get_client_dao)
):
    """
    Handles the WebSocket connection for notifications.
    
    Workflow:
      1. Validates that the client exists.
      2. Connects the client's WebSocket.
      3. Creates a consumer group for the user's notification stream.
      4. Fetches and sends any pending notifications.
      5. Starts a background task to listen and deliver real-time notifications.
      6. Processes incoming client messages (echo implementation).
      7. On disconnect, logs and does necessary cleanup.
    """
    # Validate client existence.
    client = await client_dao.get_client_by_name(client_name.lower())
    if not client:
        logger.error("Client with name '%s' not found.", client_name)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    logger.info("Client: %s", client)

    # Connect the WebSocket using our connection manager.
    await manager.connect(websocket, user_id)

    logger.info("WebSocket connected for user %s", user_id)

    # Create the consumer group (if it doesn't exist) for the user's stream.
    try:
        await create_consumer_group(user_id)
        logger.info("Consumer group created for user %s", user_id)
    except Exception as e:
        logger.error("Failed to create consumer group for user %s: %s", user_id, e)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return

    # Fetch and deliver any pending notifications.
    try:
        pending = await get_pending_notifications(user_id)
        if pending:
            for msg_id, data in pending:
                message = data.get("message")
                if message:
                    # Send a JSON payload with the message and its unique message_id.
                    await websocket.send_json({"message_id": msg_id, "message": message})
        # Do not automatically acknowledge notifications here.
    except Exception as e:
        logger.error("Error processing pending notifications for user %s: %s", user_id, e)

    # Start a background task for listening to real-time notifications.
    listener_task = asyncio.create_task(listen_for_notifications(user_id, websocket))

    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages.
            await publish_message(user_id, f"[Echo] {data}")
    except WebSocketDisconnect as e:
        logger.info("WebSocket disconnected: %s", e)
    except Exception as e:
        logger.error("Unexpected error on WebSocket connection: %s", e)
    finally:
        await manager.disconnect(websocket, user_id)
        listener_task.cancel()