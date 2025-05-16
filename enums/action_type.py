from enum import Enum


class ActionType(str, Enum):
    OPEN_URL = "open_url"
    DISMISS = "dismiss"
    MARK_READ = "mark_read"
    RETRY = "retry"
    COPY_TO_CLIPBOARD = "copy_to_clipboard"
    TRIGGER_EVENT = "trigger_event"
    LAUNCH_MODAL = "launch_modal"
    DOWNLOAD_FILE = "download_file"
    API_CALL = "api_call"
