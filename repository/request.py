from string import Template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from typing import List, Optional
from uuid import UUID
from fastapi import status

from models import Request
from enums.notification_status import NotificationStatus
from constants.error_codes import ErrorCodes
from constants.error_messages import ErrorMessages
from exception.db_exception import DBException
from models.channel import Channel
from models.client import Client
from models.provider import Provider
from models.receiver import Receiver


class RequestDAO:
    def __init__(self, session: AsyncSession):
        """
        Data Access Object for handling Request-related database operations.
        """
        self.session = session

    async def create_request(
        self,
        client_id: UUID,
        channel_id: UUID,
        receiver_id: UUID,
        payload: dict,
        provider_id: Optional[UUID] = None,
        template_id: Optional[UUID] = None,
        request_source: Optional[str] = None
    ) -> Optional[Request]:
        """
        Create a new request in the database after verifying related entities exist.

        Args:
            client_id (UUID): The ID of the client.
            channel_id (UUID): The ID of the channel.
            receiver_id (UUID): The ID of the receiver.
            payload (dict): The payload for the request.
            provider_id (Optional[UUID]): The ID of the provider (optional).
            template_id (Optional[UUID]): The ID of the template (optional).
            request_source (Optional[str]): The source of the request (optional).

        Returns:
            Optional[Request]: The created Request object.
        """
        try:
            # Check if client exists
            client_result = await self.session.execute(
                select(Client).filter(Client.id == client_id)
            )
            client = client_result.scalars().first()
            if not client:
                raise DBException(
                    error_code=ErrorCodes.Request.CREATE_FAILED,
                    error_message=ErrorMessages.Client.NOT_FOUND,
                    error={"client_id": str(client_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Check if channel exists
            channel_result = await self.session.execute(
                select(Channel).filter(Channel.id == channel_id)
            )
            channel = channel_result.scalars().first()
            if not channel:
                raise DBException(
                    error_code=ErrorCodes.Request.CREATE_FAILED,
                    error_message=ErrorMessages.Channel.NOT_FOUND,
                    error={"channel_id": str(channel_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Check if receiver exists
            receiver_result = await self.session.execute(
                select(Receiver).filter(Receiver.id == receiver_id)
            )
            receiver = receiver_result.scalars().first()
            if not receiver:
                raise DBException(
                    error_code=ErrorCodes.Request.CREATE_FAILED,
                    error_message=ErrorMessages.Receiver.NOT_FOUND,
                    error={"receiver_id": str(receiver_id)},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Check if provider exists (if provided)
            if provider_id:
                provider_result = await self.session.execute(
                    select(Provider).filter(Provider.id == provider_id)
                )
                provider = provider_result.scalars().first()
                if not provider:
                    raise DBException(
                        error_code=ErrorCodes.Request.CREATE_FAILED,
                        error_message=ErrorMessages.Provider.NOT_FOUND,
                        error={"provider_id": str(provider_id)},
                        status_code=status.HTTP_404_NOT_FOUND
                    )

            # Check if template exists (if provided)
            if template_id:
                template_result = await self.session.execute(
                    select(Template).filter(Template.id == template_id)
                )
                template = template_result.scalars().first()
                if not template:
                    raise DBException(
                        error_code=ErrorCodes.Request.CREATE_FAILED,
                        error_message=ErrorMessages.Template.NOT_FOUND,
                        error={"template_id": str(template_id)},
                        status_code=status.HTTP_404_NOT_FOUND
                    )

            # Create the request if all checks pass
            request = Request(
                client_id=client_id,
                channel_id=channel_id,
                provider_id=provider_id,
                receiver_id=receiver_id,
                template_id=template_id,
                payload=payload,
                request_source=request_source
            )
            self.session.add(request)
            await self.session.commit()
            await self.session.refresh(request)
            return request

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Request.CREATE_FAILED,
                error_message=ErrorMessages.Request.CREATE_FAILED,
                error=str(e)
            )

    async def get_request_by_id(self, request_id: UUID) -> Optional[Request]:
        """
        Retrieve a request by its ID.

        Args:
            request_id (UUID): The ID of the request.

        Returns:
            Optional[Request]: The Request object if found, else None.
        """
        try:
            result = await self.session.execute(
                select(Request).filter(Request.id == request_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise DBException(
                error_code=ErrorCodes.Request.GET_BY_ID_FAILED,
                error_message=ErrorMessages.Request.GET_BY_ID_FAILED,
                error=str(e)
            )

    async def get_requests_by_receiver_id(self, receiver_id: UUID) -> List[Request]:
        """
        Retrieve all requests for a specific receiver.

        Args:
            receiver_id (UUID): The ID of the receiver.

        Returns:
            List[Request]: A list of Request objects.
        """
        try:
            result = await self.session.execute(
                select(Request).filter(Request.receiver_id == receiver_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DBException(
                error_code=ErrorCodes.Request.GET_BY_RECEIVER_FAILED,
                error_message=ErrorMessages.Request.GET_BY_RECEIVER_FAILED,
                error=str(e)
            )

    async def update_status(
        self, request_id: UUID, status: NotificationStatus, error_message: Optional[str] = None
    ) -> None:
        """
        Update the status of a request and optionally set an error message.

        Args:
            request_id (UUID): The ID of the request.
            status (NotificationStatus): The new status of the request.
            error_message (Optional[str]): An optional error message.

        Returns:
            None
        """
        try:
            stmt = (
                update(Request)
                .where(Request.id == request_id)
                .values(status=status, error_message=error_message)
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DBException(
                error_code=ErrorCodes.Request.STATUS_UPDATE_FAILED,
                error_message=ErrorMessages.Request.STATUS_UPDATE_FAILED,
                error=str(e)
            )
