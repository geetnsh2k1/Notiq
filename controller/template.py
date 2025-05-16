import logging
from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Depends

from constants.endpoints import Endpoints
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from dependencies.authentication import get_superuser
from dependencies.dao import get_template_dao
from exception.app_exception import AppException
from mappers.template import TemplateMapper
from models.template import Template
from repository.template import TemplateDAO
from schema.base import ErrorResponse, Response
from schema.template import (
    TemplateCreate,
    TemplateDetailsResponse,
    TemplateDetailsListResponse,
    TemplateUpdate
)

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Template"],
)

@router.post(
    path=Endpoints.Template.BASE,
    response_model=TemplateDetailsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new template",
    description="Creates a new template after verifying the associated channel and provider exist.",
    responses={
        201: {"description": "Template created successfully", "model": TemplateDetailsResponse},
        400: {"description": "Bad request", "model": ErrorResponse},
        404: {"description": "Channel or provider not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def register_template(
    template_create: TemplateCreate,
    admin_user: str = Depends(get_superuser),
    template_dao: TemplateDAO = Depends(get_template_dao),
) -> TemplateDetailsResponse:
    """
    Register a new template.
    """
    template_model: Template = TemplateMapper.template_create_to_model(template_create=template_create)
    template_created: Template = await template_dao.create_template(template=template_model)
    return TemplateDetailsResponse(
        data=TemplateMapper.model_to_template_response(template=template_created),
        message="Template created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    path=Endpoints.Template.DETAILS,
    response_model=TemplateDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Update template",
    description="Updates an existing template with new data.",
    responses={
        200: {"description": "Template updated successfully", "model": TemplateDetailsResponse},
        404: {"description": "Template not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def update_template(
    template_id: UUID,
    template_update: TemplateUpdate,
    admin_user: str = Depends(get_superuser),
    template_dao: TemplateDAO = Depends(get_template_dao),
) -> TemplateDetailsResponse:
    """
    Update an existing template.
    
    Args:
        template_id (UUID): The ID of the template to update.
        template_update (TemplateUpdate): The DTO with fields to update.
    
    Returns:
        TemplateDetailsResponse: The updated template details.
    """
    existing_template: Template = await template_dao.get_template_by_id(template_id)
    if not existing_template:
        raise AppException(
            error_code=ErrorCodes.Template.NOT_FOUND,
            error_message=ErrorMessages.Template.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"Template with id '{template_id}' not found.",
        )
    
    # Update the fields if provided
    update_data = template_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_template, field, value)

    updated_template: Template = await template_dao.update_template(template=existing_template)
    return TemplateDetailsResponse(
        data=TemplateMapper.model_to_template_response(template=updated_template),
        message="Template updated successfully",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    path=Endpoints.Template.BASE,
    response_model=TemplateDetailsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all templates",
    description="Retrieves all templates.",
    responses={
        200: {"description": "Templates retrieved successfully", "model": TemplateDetailsListResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_all_templates(
    admin_user: str = Depends(get_superuser),
    template_dao: TemplateDAO = Depends(get_template_dao),
) -> TemplateDetailsListResponse:
    """
    Retrieve all templates.
    """
    templates: List[Template] = await template_dao.get_all_templates()
    template_list = [TemplateMapper.model_to_template_response(template=t) for t in templates]
    return TemplateDetailsListResponse(
        data=template_list,
        message="Templates retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    path=Endpoints.Template.GET_BY_CHANNEL,
    response_model=TemplateDetailsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get templates for a channel",
    description="Retrieves all templates associated with the given channel ID.",
    responses={
        200: {"description": "Templates retrieved successfully", "model": TemplateDetailsListResponse},
        404: {"description": "Templates not found for the channel", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_templates_by_channel(
    channel_id: UUID,
    admin_user: str = Depends(get_superuser),
    template_dao: TemplateDAO = Depends(get_template_dao),
) -> TemplateDetailsListResponse:
    """
    Retrieve templates for a specific channel.
    """
    templates: List[Template] = await template_dao.get_templates_by_channel_id(channel_id=channel_id)
    if not templates:
        raise AppException(
            error_code=ErrorCodes.Template.NOT_FOUND,
            error_message=ErrorMessages.Template.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"No templates found for channel id '{channel_id}'.",
        )
    template_list = [TemplateMapper.model_to_template_response(template=t) for t in templates]
    return TemplateDetailsListResponse(
        data=template_list,
        message="Templates retrieved successfully",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    path=Endpoints.Template.GET_BY_PROVIDER,
    response_model=TemplateDetailsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get templates for a provider",
    description="Retrieves all templates associated with the given provider ID.",
    responses={
        200: {"description": "Templates retrieved successfully", "model": TemplateDetailsListResponse},
        404: {"description": "Templates not found for the provider", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
)
async def get_templates_by_provider(
    provider_id: UUID,
    admin_user: str = Depends(get_superuser),
    template_dao: TemplateDAO = Depends(get_template_dao),
) -> TemplateDetailsListResponse:
    """
    Retrieve templates for a specific provider.
    """
    templates: List[Template] = await template_dao.get_templates_by_provider_id(provider_id=provider_id)
    if not templates:
        raise AppException(
            error_code=ErrorCodes.Template.NOT_FOUND,
            error_message=ErrorMessages.Template.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"No templates found for provider id '{provider_id}'.",
        )
    template_list = [TemplateMapper.model_to_template_response(template=t) for t in templates]
    return TemplateDetailsListResponse(
        data=template_list,
        message="Templates retrieved successfully",
        status_code=status.HTTP_200_OK,
    )
