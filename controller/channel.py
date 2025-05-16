import logging
from uuid import UUID

from fastapi import APIRouter, status, Depends

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_superuser
from dependencies.dao import get_channel_dao
from exception.app_exception import AppException
from mappers.channel import ChannelMapper
from models.channel import Channel
from repository.channel import ChannelDAO
from schema.base import ErrorResponse, Response
from schema.channel import ChannelCreate, ChannelDetails, ChannelDetailsResponse
  

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Channel"],
)

@router.post(
    path=Endpoints.Channel.CREATE,
    response_model=ChannelDetailsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new channel",
    description="Creates a new channel.",
    responses={
        201: {"description": "Channel created successfully", "model": ChannelDetailsResponse},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        400: {"description": "Bad request", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def create_channel(
    channel_create: ChannelCreate,
    admin_user: str = Depends(get_superuser),
    channel_dao: ChannelDAO = Depends(get_channel_dao),
):
    """
    Create a new channel.
    """
    channel_model: Channel = ChannelMapper.channel_create_to_model(
        channel_create=channel_create,
    )

    await channel_dao.create_channel(channel=channel_model)

    return ChannelDetailsResponse(
        data=ChannelMapper.model_to_channel_response(channel=channel_model),
        message="Channel created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.delete(
    path=Endpoints.Channel.MARK_CHANNEL_INACTIVE,
    response_model=Response,
    status_code=status.HTTP_200_OK,
    summary="Mark channel inactive (soft delete)",
    description="Marks a channel as inactive without deleting the record.",
    responses={
        200: {"description": "Channel marked inactive successfully", "model": Response},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        404: {"description": "Channel not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def soft_delete_channel(
    channel_id: UUID,
    admin_user: str = Depends(get_superuser),
    channel_dao: ChannelDAO = Depends(get_channel_dao),
):
    """
    Soft delete a channel by marking it as inactive.
    Returns the channel name.
    """
    channel = await channel_dao.get_channel_by_id(channel_id=channel_id)
    if channel is None:
        raise AppException(
            error_code=ErrorCodes.Channel.NOT_FOUND,
            error_message=ErrorMessages.Channel.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Channel with id {channel_id} not found.",
        )

    updated_channel = await channel_dao.update_channel_status(
        channel_id=channel_id,
        is_active=False
    )

    return Response(
        data=updated_channel.name,
        message="Channel marked inactive successfully",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    path=Endpoints.Channel.GET_BY_NAME,
    response_model=ChannelDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get channel details by name",
    description="Retrieve channel details using the channel name.",
    responses={
        200: {"description": "Channel details retrieved successfully", "model": ChannelDetailsResponse},
        404: {"description": "Channel not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_channel_by_name(
    name: str,
    admin_user: str = Depends(get_superuser),
    channel_dao: ChannelDAO = Depends(get_channel_dao),
):
    """
    Retrieve channel details by channel name.
    """
    channel = await channel_dao.get_channel_by_name(
        name=name.lower(),
    )
    if channel is None:
        raise AppException(
            error_code=ErrorCodes.Channel.NOT_FOUND,
            error_message=ErrorMessages.Channel.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Channel with name {name} not found.",
        )

    # Optionally map the channel model to a response schema (ChannelResponse)
    return ChannelDetailsResponse(
        data=ChannelMapper.model_to_channel_response(channel=channel),
        message="Channel details retrieved successfully",
        status_code=status.HTTP_200_OK,
    )