from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repository.client import ClientDAO
from repository.channel import ChannelDAO
from repository.provider import ProviderDAO
from repository.receiver import ReceiverDAO
from repository.request import RequestDAO
from repository.template import TemplateDAO

async def get_client_dao(
    db: AsyncSession = Depends(get_db)
) -> ClientDAO:
    return ClientDAO(db)

async def get_channel_dao(
    db: AsyncSession = Depends(get_db)
) -> ChannelDAO:
    return ChannelDAO(db)

async def get_provider_dao(
    db: AsyncSession = Depends(get_db)
) -> ProviderDAO:
    return ProviderDAO(db)

async def get_receiver_dao(
    db: AsyncSession = Depends(get_db)
) -> ReceiverDAO:
    return ReceiverDAO(db)

async def get_request_dao(
    db: AsyncSession = Depends(get_db)
) -> RequestDAO:
    return RequestDAO(db)

async def get_template_dao(
    db: AsyncSession = Depends(get_db)
) -> TemplateDAO:
    return TemplateDAO(db)