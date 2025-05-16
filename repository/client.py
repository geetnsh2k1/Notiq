from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID
from fastapi import status

from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from models import Client
from exception.db_exception import DBException


class ClientDAO:
    """
    Data Access Object for handling Client-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_client(self, client: Client) -> Optional[Client]:
        """
        Create a new client in the database.

        Args:
            client (Client): The client object to be created.

        Returns:
            Optional[Client]: The created Client object.
        """
        try:
            self.session.add(client)
            await self.session.commit()
            await self.session.refresh(client)
            return client
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.CREATE_FAILED,
                error_message=ErrorMessages.Client.CREATE_FAILED,
                error=str(e)
            )

    async def get_client_by_id(self, client_id: UUID) -> Optional[Client]:
        """
        Retrieve a client by its ID.

        Args:
            client_id (UUID): The ID of the client.

        Returns:
            Optional[Client]: The Client object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Client).filter(Client.id == client_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Client.GET_BY_ID_FAILED,
                error=str(e)
            )

    async def get_client_by_api_key(self, api_key: str) -> Optional[Client]:
        """
        Retrieve a client by its API key.

        Args:
            api_key (str): The API key of the client.

        Returns:
            Optional[Client]: The Client object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Client).filter(Client.api_key == api_key)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.GET_BY_API_KEY_FAILED,
                error_message=ErrorMessages.Client.GET_BY_API_KEY_FAILED,
                error=str(e)
            )

    async def get_client_by_name(self, client_name: str) -> Optional[Client]:
        """
        Retrieve a client by its name (case-insensitive).

        Args:
            client_name (str): The name of the client.

        Returns:
            Optional[Client]: The Client object if found, else None.
        """
        try:
            from sqlalchemy import func
            result = await self.session.execute(
                select(Client).filter(Client.client_name == client_name.lower())
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.GET_BY_NAME_FAILED,
                error_message=ErrorMessages.Client.GET_BY_NAME_FAILED,
                error=str(e)
            )

    async def update_client_status(self, client_id: UUID, is_active: bool) -> Optional[Client]:
        """
        Update the status of a client.

        Args:
            client_id (UUID): The ID of the client.
            is_active (bool): The new status of the client.

        Returns:
            Optional[Client]: The updated Client object.
        """
        try:
            client = await self.get_client_by_id(client_id)
            if client:
                client.is_active = is_active
                await self.session.commit()
                return client
            else:
                raise DBException(
                    error_code=ErrorCodes.Client.NOT_FOUND,
                    error_message=ErrorMessages.Client.NOT_FOUND_FOR_UPDATE,
                    error={"client_id": str(client_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.UPDATE_STATUS_FAILED,
                error_message=ErrorMessages.Client.UPDATE_STATUS_FAILED,
                error=str(e)
            )

    async def get_all_clients(self) -> List[Client]:
        """
        Retrieve all clients from the database.

        Returns:
            List[Client]: A list of Client objects.
        """
        try:
            result = await self.session.execute(select(Client))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.GET_ALL_FAILED,
                error_message=ErrorMessages.Client.GET_ALL_FAILED,
                error=str(e)
            )

    async def update_client(self, client: Client) -> Client:
        """
        Update and save the details of an existing client.

        Args:
            client (Client): The Client object with updated fields.

        Returns:
            Client: The updated Client object.

        Raises:
            DBException: If the update operation fails.
        """
        try:
            await self.session.commit()
            await self.session.refresh(client)
            return client
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.UPDATE_FAILED,
                error_message=ErrorMessages.Client.UPDATE_FAILED,
                error=str(e)
            )

    async def delete_client_by_id(self, client_id: UUID) -> bool:
        """
        Delete a client by its ID.

        Args:
            client_id (UUID): The ID of the client to delete.

        Returns:
            bool: True if the client was deleted, False otherwise.
        """
        try:
            client = await self.get_client_by_id(client_id)
            if client:
                await self.session.delete(client)
                await self.session.commit()
                return True
            else:
                raise DBException(
                    error_code=ErrorCodes.Client.NOT_FOUND,
                    error_message=ErrorMessages.Client.NOT_FOUND_FOR_DELETE,
                    error={"client_id": str(client_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Client.DELETE_FAILED,
                error_message=ErrorMessages.Client.DELETE_FAILED,
                error=str(e)
            )
