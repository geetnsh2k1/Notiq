import logging
from fastapi import APIRouter, Depends
from fastapi import status

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_client
from dependencies.dao import get_channel_dao, get_receiver_dao, get_request_dao
from exception.app_exception import AppException
from models.client import Client
from repository.channel import ChannelDAO
from repository.receiver import ReceiverDAO
from repository.request import RequestDAO
from schema.notification import AcknowledgeRequest, AcknowledgeResponse, NotificationRequestData, NotificationResponse, NotificationData
from websocket_manager.streams import acknowledge_notifications, publish_message

from mappers.receiver import ReceiverMapper
from schema.receiver import ReceiverCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Notification"],
)

@router.post(
    path=Endpoints.Notification.SEND,
    summary="Send Notification",
    description="Sends a notification. Requires x-api-key and user-id headers along with notification data.",
    response_model=NotificationResponse,
)
async def send_notification(
    notification: NotificationRequestData,
    client: Client = Depends(get_client),
    channel_dao: ChannelDAO = Depends(get_channel_dao),
    receiver_dao: ReceiverDAO = Depends(get_receiver_dao),
    request_dao: RequestDAO = Depends(get_request_dao)
) -> NotificationResponse:
    """
    Endpoint to send a notification. Validates the API key and user headers 
    then publishes the notification message to the user's Redis stream.
    Additionally, creates a new request record with:
      1. client_id from the client,
      2. channel fetched by name "push_notification",
      3. receiver created using the notification's user_id.
    
    Args:
        notification (NotificationRequestData): The notification payload.
        client (Client): The authenticated client.
        channel_dao: DAO for channel operations.
        receiver_dao: DAO for receiver operations.
        request_dao: DAO for request operations.
    
    Returns:
        NotificationResponse: A status message along with the user id and message id.
    """
    logger.info(
        "Notification request from: %s for user %s: %s",
        client.client_name, notification.user_id, notification.message
    )
    # Publish message and capture the message id returned from redis
    message_id = await publish_message(
        user_id=notification.user_id,
        message=notification.model_dump_json(exclude_unset=True)
    )
    
    # Fetch channel by name "push_notification"
    channel = await channel_dao.get_channel_by_name("push_notification")
    if not channel:
        raise AppException(
            error_code=ErrorCodes.Channel.NOT_FOUND,
            error_message=ErrorMessages.Channel.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error="Channel 'push_notification' not found"
        )
    
    # Check if a receiver already exists for client.id and notification.user_id
    receiver_found = await receiver_dao.get_receiver_by_client_id_and_identifier(
        client.id, notification.user_id
    )
    if receiver_found:
        receiver_created = receiver_found
    else:
        # Create new receiver entry using client.id and notification.user_id
        receiver_create = ReceiverCreate(
            client_id=client.id,
            user_id=notification.user_id
        )
        receiver_model = ReceiverMapper.receiver_create_to_model(receiver_create)
        receiver_created = await receiver_dao.create_receiver(receiver_model)
    
    # Create a new request record for the notification
    await request_dao.create_request(
        client_id=client.id,
        channel_id=channel.id,
        receiver_id=receiver_created.id,
        payload=notification.model_dump(exclude_unset=True),
        request_source="notification",
    )
    
    return NotificationResponse(
        status_code=200,
        message="Notification sent successfully",
        data=NotificationData(
            user_id=notification.user_id,
            message_id=message_id
        )
    )


@router.post(
    path=Endpoints.Notification.ACKNOWLEDGE,
    summary="Acknowledge Notifications",
    description=(
        "Explicit endpoint to acknowledge notifications retrieved from the Redis stream. "
        "Provide the user ID along with the list of message IDs to manually acknowledge the notifications."
    ),
    response_model=AcknowledgeResponse,
    status_code=status.HTTP_200_OK,
)
async def acknowledge_notification(
    req: AcknowledgeRequest,
    client: Client = Depends(get_client),
) -> AcknowledgeResponse:
    """
    Endpoint to explicitly acknowledge notifications.
    Call this endpoint with the user ID and message IDs that should be acknowledged.
    """
    try:
        await acknowledge_notifications(req.user_id, req.message_ids)
    except Exception as e:
        raise AppException(
            error_code=ErrorCodes.Request.STATUS_UPDATE_FAILED,
            error_message=ErrorMessages.Request.STATUS_UPDATE_FAILED,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e)
        )
    return AcknowledgeResponse(
        status_code=200,
        message="Notifications acknowledged successfully",
        data=True
    )