from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from schema.base import Response

class ChannelCreate(BaseModel):
    name: str = Field(..., description="Name of the channel")
    description: Optional[str] = Field(None, description="Description of the channel")

class ChannelDetails(BaseModel):
    id: UUID = Field(..., description="Channel's unique identifier")
    name: str = Field(..., description="Name of the channel")
    description: Optional[str] = Field(None, description="Description of the channel")

class ChannelDetailsResponse(Response):
    data: ChannelDetails = Field(..., description="Channel details")