from uuid import UUID
from pydantic import BaseModel, Field

class ClientCreate(BaseModel):
    client_name: str = Field(..., description="Name of the client")

class ClientDetails(BaseModel):
    id: UUID = Field(..., description="Client's unique identifier")
    client_name: str = Field(..., description="Name of the client")
