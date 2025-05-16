from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID
from fastapi import status

from models.template import Template
from models.channel import Channel
from models.provider import Provider
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.db_exception import DBException


class TemplateDAO:
    """
    Data Access Object for handling Template-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_template(self, template: Template) -> Optional[Template]:
        """
        Create a new template in the database after verifying that both the channel and provider exist.

        Args:
            template (Template): The Template object to be created.

        Returns:
            Optional[Template]: The created Template object.
        """
        try:
            # Verify channel exists
            channel_result = await self.session.execute(
                select(Channel).filter(Channel.id == template.channel_id)
            )
            channel = channel_result.scalars().first()
            if not channel:
                raise DBException(
                    error_code=ErrorCodes.Template.CREATE_FAILED,
                    error_message=ErrorMessages.Channel.NOT_FOUND,
                    error={"channel_id": str(template.channel_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
            # Verify provider exists
            provider_result = await self.session.execute(
                select(Provider).filter(Provider.id == template.provider_id)
            )
            provider = provider_result.scalars().first()
            if not provider:
                raise DBException(
                    error_code=ErrorCodes.Template.CREATE_FAILED,
                    error_message=ErrorMessages.Provider.NOT_FOUND,
                    error={"provider_id": str(template.provider_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Add the template to the session and commit
            self.session.add(template)
            await self.session.commit()
            await self.session.refresh(template)
            return template
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.CREATE_FAILED,
                error_message=ErrorMessages.Template.CREATE_FAILED,
                error=str(e)
            )

    async def get_template_by_id(self, template_id: UUID) -> Optional[Template]:
        """
        Retrieve a template by its ID.

        Args:
            template_id (UUID): The ID of the template.

        Returns:
            Optional[Template]: The Template object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Template).filter(Template.id == template_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Template.GET_BY_ID_FAILED,
                error=str(e)
            )

    async def get_all_templates(self) -> List[Template]:
        """
        Retrieve all templates from the database.

        Returns:
            List[Template]: A list of Template objects.
        """
        try:
            result = await self.session.execute(select(Template))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.GET_ALL_FAILED,
                error_message=ErrorMessages.Template.GET_ALL_FAILED,
                error=str(e)
            )

    async def get_templates_by_channel_id(self, channel_id: UUID) -> List[Template]:
        """
        Retrieve all templates associated with a specific channel.

        Args:
            channel_id (UUID): The ID of the channel.

        Returns:
            List[Template]: A list of Template objects.
        """
        try:
            result = await self.session.execute(
                select(Template).filter(Template.channel_id == channel_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.GET_BY_CHANNEL_ID_FAILED,
                error_message=ErrorMessages.Template.GET_BY_CHANNEL_ID_FAILED,
                error=str(e)
            )

    async def get_templates_by_provider_id(self, provider_id: UUID) -> List[Template]:
        """
        Retrieve all templates associated with a specific provider.

        Args:
            provider_id (UUID): The ID of the provider.

        Returns:
            List[Template]: A list of Template objects.
        """
        try:
            result = await self.session.execute(
                select(Template).filter(Template.provider_id == provider_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.GET_BY_PROVIDER_ID_FAILED,
                error_message=ErrorMessages.Template.GET_BY_PROVIDER_ID_FAILED,
                error=str(e)
            )

    async def update_template(self, template: Template) -> Optional[Template]:
        """
        Update and save the details of an existing template in the database.

        Args:
            template (Template): The Template object with updated fields.

        Returns:
            Optional[Template]: The updated Template object.

        Raises:
            DBException: If the update operation fails.
        """
        try:
            await self.session.commit()
            await self.session.refresh(template)
            return template
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.UPDATE_FAILED,
                error_message=ErrorMessages.Template.UPDATE_FAILED,
                error=str(e)
            )
    
    async def delete_template_by_id(self, template_id: UUID) -> bool:
        """
        Delete a template by its ID.

        Args:
            template_id (UUID): The ID of the template to delete.

        Returns:
            bool: True if the template was deleted, False otherwise.
        """
        try:
            template = await self.get_template_by_id(template_id)
            if template:
                await self.session.delete(template)
                await self.session.commit()
                return True
            else:
                raise DBException(
                    error_code=ErrorCodes.Template.NOT_FOUND,
                    error_message=ErrorMessages.Template.NOT_FOUND_FOR_DELETE,
                    error={"template_id": str(template_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Template.DELETE_FAILED,
                error_message=ErrorMessages.Template.DELETE_FAILED,
                error=str(e)
            )
