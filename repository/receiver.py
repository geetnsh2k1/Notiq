from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID
from fastapi import status

from models import Receiver
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.db_exception import DBException
from models.client import Client


class ReceiverDAO:
    """
    Data Access Object for handling Receiver-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_receiver(self, receiver: Receiver) -> Optional[Receiver]:
        """
        Create a new receiver in the database after verifying that the associated client exists.

        Args:
            receiver (Receiver): The Receiver object to be created.

        Returns:
            Optional[Receiver]: The created Receiver object.
        """
        try:
            # Check if the associated client exists
            client_result = await self.session.execute(
                select(Client).filter(Client.id == receiver.client_id)
            )
            client = client_result.scalars().first()
            if not client:
                raise DBException(
                    error_code=ErrorCodes.Receiver.CREATE_FAILED,
                    error_message=ErrorMessages.Client.NOT_FOUND,
                    error={"client_id": str(receiver.client_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Add the receiver to the session and commit the transaction
            self.session.add(receiver)
            await self.session.commit()
            await self.session.refresh(receiver)
            return receiver
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Receiver.CREATE_FAILED,
                error_message=ErrorMessages.Receiver.CREATE_FAILED,
                error=str(e)
            )

    async def get_receiver_by_id(self, receiver_id: UUID) -> Optional[Receiver]:
        """
        Retrieve a receiver by its ID.

        Args:
            receiver_id (UUID): The ID of the receiver.

        Returns:
            Optional[Receiver]: The Receiver object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Receiver).filter(Receiver.id == receiver_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Receiver.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Receiver.GET_BY_ID_FAILED,
                error=str(e)
            )

    async def get_receivers_by_client_id(self, client_id: UUID) -> List[Receiver]:
        """
        Retrieve all receivers for a specific client.

        Args:
            client_id (UUID): The ID of the client.

        Returns:
            List[Receiver]: A list of Receiver objects.
        """
        try:
            result = await self.session.execute(
                select(Receiver).filter(Receiver.client_id == client_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Receiver.GET_BY_CLIENT_ID_FAILED,
                error_message=ErrorMessages.Receiver.GET_BY_CLIENT_ID_FAILED,
                error=str(e)
            )

    async def get_receiver_by_client_id_and_identifier(self, client_id: UUID, identifier: str) -> Optional[Receiver]:
        """
        Retrieve a receiver by client_id and identifier. The identifier can match user_id, email, or phone_number.
        
        Args:
            client_id (UUID): The client's ID.
            identifier (str): The identifier to match against receiver's user_id, email, or phone_number.
        
        Returns:
            Optional[Receiver]: The matched Receiver object, or None if not found.
        """
        try:
            result = await self.session.execute(
                select(Receiver).filter(
                    Receiver.client_id == client_id,
                    or_(
                        Receiver.user_id == identifier,
                        Receiver.email == identifier,
                        Receiver.phone_number == identifier
                    )
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Receiver.GET_BY_CLIENT_ID_FAILED,
                error_message=ErrorMessages.Receiver.GET_BY_CLIENT_ID_FAILED,
                error=str(e)
            )

    async def delete_receiver_by_id(self, receiver_id: UUID) -> bool:
        """
        Delete a receiver by its ID.

        Args:
            receiver_id (UUID): The ID of the receiver to delete.

        Returns:
            bool: True if the receiver was deleted, False otherwise.
        """
        try:
            receiver = await self.get_receiver_by_id(receiver_id)
            if receiver:
                await self.session.delete(receiver)
                await self.session.commit()
                return True
            else:
                raise DBException(
                    error_code=ErrorCodes.Receiver.NOT_FOUND,
                    error_message=ErrorMessages.Receiver.NOT_FOUND_FOR_DELETE,
                    error={"receiver_id": str(receiver_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Receiver.DELETE_FAILED,
                error_message=ErrorMessages.Receiver.DELETE_FAILED,
                error=str(e)
            )
