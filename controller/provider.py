import logging
from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import SQLAlchemyError

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_superuser
from dependencies.dao import get_provider_dao
from exception.app_exception import AppException
from mappers.provider import ProviderMapper
from models.provider import Provider
from repository.provider import ProviderDAO 
from schema.base import ErrorResponse, Response
from schema.provider import (
    ProviderCreate,
    ProviderDetailsListResponse,
    ProviderDetailsResponse
)

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Provider"],
)


@router.post(
    path=Endpoints.Provider.CREATE,
    response_model=ProviderDetailsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new provider",
    description="Creates a new provider, verifies the associated channel exists, and returns the provider's details.",
    responses={
        201: {"description": "Provider created successfully", "model": ProviderDetailsResponse},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        400: {"description": "Bad request", "model": ErrorResponse},
        404: {"description": "Channel not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def create_provider(
    provider_create: ProviderCreate,
    admin_user: str = Depends(get_superuser),
    provider_dao: ProviderDAO = Depends(get_provider_dao),
) -> ProviderDetailsResponse:
    """
    Endpoint to create a new provider.

    Args:
        provider_create (ProviderCreate): DTO for creating a provider.
        admin_user (str): The authenticated superuser.
        provider_dao (ProviderDAO): Data access object for provider operations.

    Returns:
        ProviderDetailsResponse: The response containing the created provider details.
    """
    # Convert the incoming DTO to a Provider model instance.
    provider_model: Provider = ProviderMapper.provider_create_to_model(
        provider_create=provider_create,
    )
    try:
        provider_created: Provider = await provider_dao.create_provider(
            provider=provider_model,
        )
    except SQLAlchemyError as exc:
        logger.error("Error creating provider: %s", exc, exc_info=True)
        raise

    response: ProviderDetailsResponse = ProviderDetailsResponse(
        data=ProviderMapper.model_to_provider_response(provider=provider_created),
        message="Provider created successfully",
        status_code=status.HTTP_201_CREATED,
    )
    return response


@router.get(
    path=Endpoints.Provider.GET_BY_NAME,
    response_model=ProviderDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get provider details by name",
    description="Retrieves provider details using the provider name.",
    responses={
        200: {"description": "Provider details retrieved successfully", "model": ProviderDetailsResponse},
        404: {"description": "Provider not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_provider_by_name(
    name: str,
    admin_user: str = Depends(get_superuser),
    provider_dao: ProviderDAO = Depends(get_provider_dao),
) -> ProviderDetailsResponse:
    """
    Endpoint to retrieve provider details by name.

    Args:
        name (str): The provider name.
        admin_user (str): The authenticated superuser.
        provider_dao (ProviderDAO): Data access object for provider operations.

    Returns:
        ProviderDetailsResponse: The response containing the retrieved provider details.
    """
    provider: Provider = await provider_dao.get_provider_by_name(name=name.lower())
    if provider is None:
        raise AppException(
            error_code=ErrorCodes.Provider.NOT_FOUND,
            error_message=ErrorMessages.Provider.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Provider with name '{name}' not found.",
        )
    return ProviderDetailsResponse(
        data=ProviderMapper.model_to_provider_response(provider=provider),
        message="Provider details retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    path=Endpoints.Provider.GET_BY_CHANNEL,
    response_model=ProviderDetailsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all providers by channel ID",
    description="Retrieves all providers associated with the given channel id.",
    responses={
        200: {"description": "Providers retrieved successfully", "model": ProviderDetailsListResponse},
        404: {"description": "Providers not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_providers_by_channel_id(
    channel_id: UUID,
    admin_user: str = Depends(get_superuser),
    provider_dao: ProviderDAO = Depends(get_provider_dao),
) -> ProviderDetailsListResponse:
    """
    Endpoint to retrieve all providers for a specific channel.

    Args:
        channel_id (UUID): The channel ID.
        admin_user (str): The authenticated superuser.
        provider_dao (ProviderDAO): Data access object for provider operations.

    Returns:
        ProviderDetailsListResponse: The response containing a list of provider details.
    """
    providers: List[Provider] = await provider_dao.get_providers_by_channel_id(channel_id=channel_id)
    if not providers:
        raise AppException(
            error_code=ErrorCodes.Provider.NOT_FOUND,
            error_message=ErrorMessages.Provider.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"No providers found for channel id '{channel_id}'.",
        )
    provider_list = [ProviderMapper.model_to_provider_response(provider=provider) for provider in providers]
    return ProviderDetailsListResponse(
        data=provider_list,
        message="Providers retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


@router.delete(
    path=Endpoints.Provider.MARK_PROVIDER_INACTIVE,
    response_model=Response,
    status_code=status.HTTP_200_OK,
    summary="Mark provider inactive",
    description="Marks a provider as inactive without deleting the record.",
    responses={
        200: {"description": "Provider marked inactive successfully", "model": Response},
        404: {"description": "Provider not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def mark_provider_inactive(
    provider_id: UUID,
    admin_user: str = Depends(get_superuser),
    provider_dao: ProviderDAO = Depends(get_provider_dao),
) -> Response:
    """
    Endpoint to mark a provider as inactive.

    Args:
        provider_id (UUID): The provider's unique identifier.
        admin_user (str): The authenticated superuser.
        provider_dao (ProviderDAO): Data access object for provider operations.

    Returns:
        Response: A response with the provider's name confirming inactivation.
    """
    provider: Provider = await provider_dao.get_provider_by_id(provider_id=provider_id)
    if provider is None:
        raise AppException(
            error_code=ErrorCodes.Provider.NOT_FOUND,
            error_message=ErrorMessages.Provider.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Provider with id '{provider_id}' not found.",
        )
    # Mark the provider as inactive.
    provider.is_active = False
    updated_provider: Provider = await provider_dao.update_provider(provider=provider)
    return Response(
        data=updated_provider.name,
        message="Provider marked inactive successfully",
        status_code=status.HTTP_200_OK,
    )