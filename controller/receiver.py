import logging
from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Depends

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_superuser
from dependencies.dao import get_receiver_dao
from exception.app_exception import AppException
from mappers.receiver import ReceiverMapper
from models.receiver import Receiver
from repository.receiver import ReceiverDAO
from schema.base import ErrorResponse, Response
from schema.receiver import (
    ReceiverDetailsListResponse,
    ReceiverDetails
)

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Receiver"],
)

@router.get(
    path=Endpoints.Receiver.GET_BY_CLIENT,
    response_model=ReceiverDetailsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all receivers by client ID",
    description="Retrieves all receivers associated with the provided client ID.",
    responses={
        200: {"description": "Receivers retrieved successfully", "model": ReceiverDetailsListResponse},
        404: {"description": "Receivers not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_receivers_by_client_id(
    client_id: UUID,
    admin_user: str = Depends(get_superuser),
    receiver_dao: ReceiverDAO = Depends(get_receiver_dao),
) -> ReceiverDetailsListResponse:
    """
    Endpoint to retrieve all receivers for a given client ID.

    Args:
        client_id (UUID): The unique identifier of the client.
        admin_user (str): The authenticated superuser.
        receiver_dao (ReceiverDAO): Data access object for receiver operations.

    Returns:
        ReceiverDetailsListResponse: A response containing a list of receiver details.
    """
    receivers: List[Receiver] = await receiver_dao.get_receivers_by_client_id(client_id=client_id)
    if not receivers:
        raise AppException(
            error_code=ErrorCodes.Receiver.NOT_FOUND,
            error_message=ErrorMessages.Receiver.NOT_FOUND_FOR_CLIENT_ID,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"No receivers found for client id '{client_id}'.",
        )
    
    # Transform each Receiver model to its Response DTO
    receiver_list: List[ReceiverDetails] = [ReceiverMapper.model_to_receiver_response(receiver=r) for r in receivers]
    
    return ReceiverDetailsListResponse(
        data=receiver_list,
        message="Receivers retrieved successfully",
        status_code=status.HTTP_200_OK,
    )