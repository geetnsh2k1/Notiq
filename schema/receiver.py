from typing import Optional, Any, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field

from schema.base import Response

class ReceiverCreate(BaseModel):
    client_id: UUID = Field(..., description="ID of the client associated with the receiver")
    user_id: Optional[str] = Field(None, description="Optional logical user identifier")
    email: Optional[str] = Field(None, description="Email address of the receiver")
    phone_number: Optional[str] = Field(None, description="Phone number of the receiver")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Extra metadata for the receiver (e.g., preferences, tags)")

class ReceiverDetails(BaseModel):
    id: UUID = Field(..., description="Receiver's unique identifier")
    client_id: UUID = Field(..., description="ID of the client associated with the receiver")
    user_id: Optional[str] = Field(None, description="Optional logical user identifier")
    email: Optional[str] = Field(None, description="Email address of the receiver")
    phone_number: Optional[str] = Field(None, description="Phone number of the receiver")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Extra metadata for the receiver")

class ReceiverDetailsResponse(Response):
    data: ReceiverDetails = Field(..., description="Receiver details")

class ReceiverDetailsListResponse(Response):
    data: List[ReceiverDetails] = Field(..., description="List of receiver details")