from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db.base import BaseModel


class Channel(BaseModel):
    __tablename__ = "channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)  # e.g., "email", "sms"
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
