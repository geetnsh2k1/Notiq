from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID
from fastapi import status

from models import Provider, Channel
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.db_exception import DBException


class ProviderDAO:
    """
    Data Access Object for handling Provider-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_provider(self, provider: Provider) -> Optional[Provider]:
        """
        Create a new provider in the database after verifying that the channel exists.

        Args:
            provider (Provider): The Provider object to be created.

        Returns:
            Optional[Provider]: The created Provider object.
        """
        try:
            # Check if the channel exists using the provider's channel_id
            channel_result = await self.session.execute(
                select(Channel).filter(Channel.id == provider.channel_id)
            )
            channel = channel_result.scalars().first()
            if not channel:
                raise DBException(
                    error_code=ErrorCodes.Provider.CREATE_FAILED,
                    error_message=ErrorMessages.Channel.NOT_FOUND,
                    error={"channel_id": str(provider.channel_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Add provider to the session and save to the database
            self.session.add(provider)
            await self.session.commit()
            await self.session.refresh(provider)
            return provider
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.CREATE_FAILED,
                error_message=ErrorMessages.Provider.CREATE_FAILED,
                error=str(e)
            )

    async def get_provider_by_id(self, provider_id: UUID) -> Optional[Provider]:
        """
        Retrieve a provider by its ID.

        Args:
            provider_id (UUID): The ID of the provider.

        Returns:
            Optional[Provider]: The Provider object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Provider).filter(Provider.id == provider_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Provider.GET_BY_ID_FAILED,
                error=str(e)
            )
    
    async def get_provider_by_name(self, name: str) -> Optional[Provider]:
        """
        Retrieve a provider by its name.

        Args:
            name (str): The name of the provider.

        Returns:
            Optional[Provider]: The Provider object if found, else None.
        """
        try:
            from sqlalchemy import func
            result = await self.session.execute(
                select(Provider).filter(func.lower(Provider.name) == name.lower())
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.GET_BY_NAME_FAILED,
                error_message=ErrorMessages.Provider.GET_BY_NAME_FAILED,
                error=str(e)
            )

    async def get_providers_by_channel_id(self, channel_id: UUID) -> List[Provider]:
        """
        Retrieve all providers for a specific channel.

        Args:
            channel_id (UUID): The ID of the channel.

        Returns:
            List[Provider]: A list of Provider objects.
        """
        try:
            result = await self.session.execute(
                select(Provider).filter(Provider.channel_id == channel_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.GET_BY_CHANNEL_ID_FAILED,
                error_message=ErrorMessages.Provider.GET_BY_CHANNEL_ID_FAILED,
                error=str(e)
            )
    
    async def get_all_providers(self) -> List[Provider]:
        """
        Retrieve all providers from the database.

        Returns:
            List[Provider]: A list of Provider objects.
        """
        try:
            result = await self.session.execute(select(Provider))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.GET_ALL_FAILED,
                error_message=ErrorMessages.Provider.GET_ALL_FAILED,
                error=str(e)
            )

    async def update_provider_status(
        self, provider_id: UUID, is_active: bool
    ) -> Optional[Provider]:
        """
        Update the status of a provider.

        Args:
            provider_id (UUID): The ID of the provider.
            is_active (bool): The new status of the provider.

        Returns:
            Optional[Provider]: The updated Provider object.
        """
        try:
            provider = await self.get_provider_by_id(provider_id)
            if provider:
                provider.is_active = is_active
                await self.session.commit()
                return provider
            else:
                raise DBException(
                    error_code=ErrorCodes.Provider.NOT_FOUND,
                    error_message=ErrorMessages.Provider.NOT_FOUND_FOR_UPDATE,
                    error={"provider_id": str(provider_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.UPDATE_STATUS_FAILED,
                error_message=ErrorMessages.Provider.UPDATE_STATUS_FAILED,
                error=str(e)
            )

    async def update_provider(self, provider: Provider) -> Optional[Provider]:
        """
        Update and save the details of an existing provider.

        Args:
            provider (Provider): The Provider object with updated fields.

        Returns:
            Optional[Provider]: The updated Provider object.
        """
        try:
            await self.session.commit()
            await self.session.refresh(provider)
            return provider
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.UPDATE_FAILED,
                error_message=ErrorMessages.Provider.UPDATE_FAILED,
                error=str(e)
            )

    async def delete_provider_by_id(self, provider_id: UUID) -> bool:
        """
        Delete a provider by its ID.

        Args:
            provider_id (UUID): The ID of the provider to delete.

        Returns:
            bool: True if the provider was deleted, False otherwise.
        """
        try:
            provider = await self.get_provider_by_id(provider_id)
            if provider:
                await self.session.delete(provider)
                await self.session.commit()
                return True
            else:
                raise DBException(
                    error_code=ErrorCodes.Provider.NOT_FOUND,
                    error_message=ErrorMessages.Provider.NOT_FOUND_FOR_DELETE,
                    error={"provider_id": str(provider_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Provider.DELETE_FAILED,
                error_message=ErrorMessages.Provider.DELETE_FAILED,
                error=str(e)
            )
