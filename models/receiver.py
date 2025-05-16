from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from db.base import BaseModel


class Receiver(BaseModel):
    __tablename__ = "receivers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # Receiver identifiers
    user_id = Column(String, nullable=True)  # optional logical ID
    email = Column(String, nullable=True, index=True)
    phone_number = Column(String, nullable=True, index=True)

    # Flexible extra meta_data (preferences, tags, etc.)
    meta_data = Column(JSONB, nullable=True)

    __table_args__ = (
        UniqueConstraint('client_id', 'user_id', name='uq_receiver_clients_user'),
    )
