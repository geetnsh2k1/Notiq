from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db.base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_name = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
