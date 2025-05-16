from sqlalchemy import Column, String, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db.base import BaseModel
from enums.notification_status import NotificationStatus


class Request(BaseModel):
    __tablename__ = "requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id", ondelete="SET NULL"), nullable=True)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("receivers.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id", ondelete="SET NULL"), nullable=True)

    payload = Column(JSON, nullable=False)

    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    error_message = Column(String, nullable=True)

    request_source = Column(String, nullable=True) # e.g., source_type + source_name
