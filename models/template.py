from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from db.base import BaseModel


class Template(BaseModel):
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)

    template_ref_id = Column(String, nullable=False)     # Provider-specific ID
    template_name = Column(String, nullable=False)   # Internal use name
    
    description = Column(Text, nullable=True)
    meta_data = Column(JSONB, nullable=True)

    # 🔐 This is the new field: JSON Schema for variable validation
    schema = Column(JSONB, nullable=True)  # JSON Schema for required variables
