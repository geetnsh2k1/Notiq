from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field

from schema.base import Response

class ProviderCreate(BaseModel):
    name: str = Field(..., description="Name of the provider")
    channel_id: UUID = Field(..., description="ID of the channel associated with the provider")
    config: dict[str, Any] = Field(..., description="Provider-specific configuration (e.g., API keys, usernames)")

class ProviderDetails(BaseModel):
    id: UUID = Field(..., description="Provider's unique identifier")
    name: str = Field(..., description="Name of the provider")
    channel_id: UUID = Field(..., description="ID of the channel associated with the provider")
    config: dict[str, Any] = Field(..., description="Provider-specific configuration")
    is_active: bool = Field(..., description="Indicates if the provider is active")

class ProviderDetailsResponse(Response):
    data: ProviderDetails = Field(..., description="Provider details")

class ProviderDetailsListResponse(Response):
    data: list[ProviderDetails] = Field(..., description="List of provider details")