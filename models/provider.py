from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from db.base import BaseModel


class Provider(BaseModel):
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # e.g., "twilio", "sendgrid"
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    config = Column(JSONB, nullable=False)  # provider-specific config like API keys, usernames, etc.
    is_active = Column(Boolean, default=True)
