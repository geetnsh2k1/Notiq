from typing import List, Optional, Dict
from pydantic import BaseModel, Field

from enums.action_type import ActionType
from enums.notification_type import NotificationType
from enums.redirection_type import RedirectionType
from schema.base import Response


class NotificationRedirection(BaseModel):
    type: RedirectionType = Field(..., description="Type of redirection: 'internal' or 'external'")
    url: str = Field(..., description="URL to redirect the user to")
    open_in_new_tab: Optional[bool] = Field(False, description="Whether the URL should open in a new browser tab")


class NotificationActionData(BaseModel):
    value: str = Field(..., description="The value to copy or use in the action")


class NotificationAction(BaseModel):
    label: str = Field(..., description="Text label for the action button")
    action: ActionType = Field(..., description="Type of action to perform")
    color_code: str = Field(..., description="Hex color code representing the button's color")
    url: Optional[str] = Field(None, description="URL to open, required if action is 'open_url'")
    data: Optional[NotificationActionData] = Field(None, description="Additional data, required if action is 'copy_to_clipboard'")


class NotificationRequestData(BaseModel):
    user_id: str = Field(..., description="Identifier of the user the notification is for")
    type: NotificationType = Field(..., description="Type of the notification (e.g., success, error, warning, info)")
    color_code: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$", description="Hex code for the notification's theme color")
    title: str = Field(..., description="Title or heading of the notification")
    message: str = Field(..., description="Main message of the notification")
    icon_url: Optional[str] = Field(None, description="URL of the icon to display in the notification")
    timeout: int = Field(..., description="Time in milliseconds before the notification auto-dismisses")
    is_sticky: bool = Field(..., description="If true, the notification remains until dismissed manually")
    redirection: Optional[NotificationRedirection] = Field(None, description="Optional redirection configuration")
    actions: Optional[List[NotificationAction]] = Field(None, description="List of user actions for the notification")
    metadata: Optional[Dict[str, str]] = Field(None, description="Optional key-value metadata for additional context")


class NotificationData(BaseModel):
    user_id: str
    message_id: str


class NotificationResponse(Response):
    data: NotificationData


class AcknowledgeRequest(BaseModel):
    user_id: str
    message_ids: List[str]

class AcknowledgeResponse(Response):
    data: bool = Field(
        ...,
        description="Indicates whether the acknowledgment was successful or not"
    )