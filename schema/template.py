from typing import Optional, Any, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field

from schema.base import Response

class TemplateCreate(BaseModel):
    channel_id: UUID = Field(..., description="ID of the channel associated with the template")
    provider_id: UUID = Field(..., description="ID of the provider associated with the template")
    template_ref_id: str = Field(..., description="Provider-specific reference ID for the template")
    template_name: str = Field(..., description="Internal name for the template")
    description: Optional[str] = Field(None, description="Description of the template")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the template")
    template_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for variable validation within the template", alias="schema")

class TemplateUpdate(BaseModel):
    template_ref_id: Optional[str] = Field(None, description="Provider-specific reference ID for the template")
    template_name: Optional[str] = Field(None, description="Internal name for the template")
    description: Optional[str] = Field(None, description="Description of the template")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the template")
    template_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for variable validation within the template", alias="schema")

class TemplateDetails(BaseModel):
    id: UUID = Field(..., description="Template's unique identifier")
    channel_id: UUID = Field(..., description="ID of the channel associated with the template")
    provider_id: UUID = Field(..., description="ID of the provider associated with the template")
    template_ref_id: str = Field(..., description="Provider-specific reference ID for the template")
    template_name: str = Field(..., description="Internal name for the template")
    description: Optional[str] = Field(None, description="Description of the template")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the template")
    template_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for variable validation within the template", alias="schema")

class TemplateDetailsResponse(Response):
    data: TemplateDetails = Field(..., description="Template details")

class TemplateDetailsListResponse(Response):
    data: List[TemplateDetails] = Field(..., description="List of template details")