from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID
from fastapi import status

from models import Channel
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.db_exception import DBException


class ChannelDAO:
    """
    Data Access Object for handling Channel-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_channel(self, channel: Channel) -> Optional[Channel]:
        """
        Create a new channel in the database.

        Args:
            channel (Channel): The Channel object to be created.

        Returns:
            Optional[Channel]: The created Channel object.
        """
        try:
            self.session.add(channel)
            await self.session.commit()
            await self.session.refresh(channel)
            return channel
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.CREATE_FAILED,
                error_message=ErrorMessages.Channel.CREATE_FAILED,
                error=str(e)
            )

    async def get_channel_by_id(self, channel_id: UUID) -> Optional[Channel]:
        """
        Retrieve a channel by its ID.

        Args:
            channel_id (UUID): The ID of the channel.

        Returns:
            Optional[Channel]: The Channel object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Channel).filter(Channel.id == channel_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Channel.GET_BY_ID_FAILED,
                error=str(e)
            )

    async def get_channel_by_name(self, name: str) -> Optional[Channel]:
        """
        Retrieve a channel by its name.

        Args:
            name (str): The name of the channel.

        Returns:
            Optional[Channel]: The Channel object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Channel).filter(Channel.name == name)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.GET_BY_NAME_FAILED,
                error_message=ErrorMessages.Channel.GET_BY_NAME_FAILED,
                error=str(e)
            )

    async def update_channel_status(self, channel_id: UUID, is_active: bool) -> Optional[Channel]:
        """
        Update the status of a channel.

        Args:
            channel_id (UUID): The ID of the channel.
            is_active (bool): The new status of the channel.

        Returns:
            Optional[Channel]: The updated Channel object.
        """
        try:
            channel = await self.get_channel_by_id(channel_id)
            if channel:
                channel.is_active = is_active
                await self.session.commit()
                return channel
            else:
                raise DBException(
                    error_code=ErrorCodes.Channel.NOT_FOUND,
                    error_message=ErrorMessages.Channel.NOT_FOUND_FOR_UPDATE,
                    error={"channel_id": str(channel_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.UPDATE_STATUS_FAILED,
                error_message=ErrorMessages.Channel.UPDATE_STATUS_FAILED,
                error=str(e)
            )

    async def get_all_channels(self) -> List[Channel]:
        """
        Retrieve all channels from the database.

        Returns:
            List[Channel]: A list of Channel objects.
        """
        try:
            result = await self.session.execute(select(Channel))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.GET_ALL_FAILED,
                error_message=ErrorMessages.Channel.GET_ALL_FAILED,
                error=str(e)
            )

    async def delete_channel_by_id(self, channel_id: UUID) -> bool:
        """
        Delete a channel by its ID.

        Args:
            channel_id (UUID): The ID of the channel to delete.

        Returns:
            bool: True if the channel was deleted, False otherwise.
        """
        try:
            channel = await self.get_channel_by_id(channel_id)
            if channel:
                await self.session.delete(channel)
                await self.session.commit()
                return True
            else:
                raise DBException(
                    error_code=ErrorCodes.Channel.NOT_FOUND,
                    error_message=ErrorMessages.Channel.NOT_FOUND_FOR_DELETE,
                    error={"channel_id": str(channel_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Channel.DELETE_FAILED,
                error_message=ErrorMessages.Channel.DELETE_FAILED,
                error=str(e)
            )
