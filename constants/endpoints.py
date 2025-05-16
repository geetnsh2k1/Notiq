class Endpoints:
    class Client:
        CREATE = "/clients"
        REGENERATE_API_KEY = "/clients/{client_id}/regenerate_api_key"
        MARK_CLIENT_INACTIVE = "/clients/{client_id}/mark_inactive"

    class Channel:
        CREATE = "/channels"
        GET_BY_NAME = "/channels/name/{name}"
        MARK_CHANNEL_INACTIVE = "/channels/{channel_id}/mark_inactive"

    class Provider:
        CREATE = "/providers"
        GET_BY_NAME = "/providers/name/{name}"
        GET_BY_CHANNEL = "/channels/{channel_id}/providers"
        MARK_PROVIDER_INACTIVE = "/providers/{provider_id}/mark_inactive"

    class Receiver:
        GET_BY_CLIENT = "/clients/{client_id}/receivers"

    class Template:
        BASE = "/templates"
        DETAILS = f"{BASE}/{{template_id}}"
        GET_BY_CHANNEL = "/channels/{channel_id}/templates"
        GET_BY_PROVIDER = "/providers/{provider_id}/templates"

    class Request:
        CREATE = "/requests"
        GET_BY_ID = "/requests/{request_id}"
        GET_BY_RECEIVER = "/receivers/{receiver_id}/requests"
        UPDATE_STATUS = "/requests/{request_id}/status"
    
    class Notification:
        SEND = "/notification/send"
        ACKNOWLEDGE = "/notification/acknowledge"

    class WebSocket:
        WS_CONNECTION = "/ws/{client_name}/{user_id}"
