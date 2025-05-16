import logging
from uuid import UUID

from fastapi import APIRouter, status, Depends

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_superuser
from dependencies.dao import get_client_dao
from exception.app_exception import AppException
from mappers.client import ClientMapper
from models.client import Client
from repository.client import ClientDAO
from schema.base import ErrorResponse, Response
from schema.client import ClientCreate
from utils.security import generate_api_key


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Client"],
)

@router.post(
    path=Endpoints.Client.CREATE,
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new client",
    description="Creates a new client and returns the raw API key.",
    responses={
        201: {"description": "Client created successfully", "model": Response},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        400: {"description": "Bad request", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def create_client(
    client_create: ClientCreate,
    admin_user: str = Depends(get_superuser),
    client_dao: ClientDAO = Depends(get_client_dao),
):
    """
    Create a new client and generate its API key.
    """
    raw_key, hashed_key = generate_api_key(
        client_name=client_create.client_name,
    )

    client_model: Client = ClientMapper.client_create_to_model(
        client_name=client_create.client_name,
        hashed_api_key=hashed_key,
    )

    # Persist the new client asynchronously
    await client_dao.create_client(client_model)

    return Response(
        data=raw_key,
        message="Client created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    path=Endpoints.Client.REGENERATE_API_KEY,
    response_model=Response,
    status_code=status.HTTP_200_OK,
    summary="Regenerate client's API key",
    description="Regenerates and updates the API key for an existing client.",
    responses={
        200: {"description": "Client API key regenerated successfully", "model": Response},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        404: {"description": "Client not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def regenerate_api_key(
    client_id: UUID,
    admin_user: str = Depends(get_superuser),
    client_dao: ClientDAO = Depends(get_client_dao),
):
    """
    Regenerate the API key for a client.
    """
    client = await client_dao.get_client_by_id(client_id)
    if client is None:
        raise AppException(
            error_code=ErrorCodes.Client.NOT_FOUND,
            error_message=ErrorMessages.Client.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Client with id {client_id} not found.",
        )

    new_api_raw_key, new_api_hashed_key = generate_api_key(
        client_name=client.client_name,
    )
    client.api_key = new_api_hashed_key

    await client_dao.update_client(client)

    return Response(
        data=new_api_raw_key,
        message="Client API key regenerated successfully",
        status_code=status.HTTP_200_OK,
    )


@router.delete(
    path=Endpoints.Client.MARK_CLIENT_INACTIVE,
    response_model=Response,
    status_code=status.HTTP_200_OK,
    summary="Mark client inactive (soft delete)",
    description="Marks a client as inactive without deleting the record.",
    responses={
        200: {"description": "Client marked inactive successfully", "model": Response},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        404: {"description": "Client not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def soft_delete_client(
    client_id: UUID,
    admin_user: str = Depends(get_superuser),
    client_dao: ClientDAO = Depends(get_client_dao),
):
    """
    Soft delete a client by marking it as inactive.
    Returns the client's name.
    """
    client = await client_dao.get_client_by_id(client_id)
    if client is None:
        raise AppException(
            error_code=ErrorCodes.Client.NOT_FOUND,
            error_message=ErrorMessages.Client.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Client with id {client_id} not found.",
        )

    # Mark the client as inactive
    updated_client = await client_dao.update_client_status(
        client_id=client_id, 
        is_active=False
    )
    return Response(
        data=updated_client.client_name,
        message="Client marked inactive successfully",
        status_code=status.HTTP_200_OK,
    )