from enum import Enum

class ErrorMessages:
    class Client(str, Enum):
        CREATE_FAILED = "We couldn't create a new client at the moment. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve the client details. Please double-check the client ID and try again."
        GET_BY_API_KEY_FAILED = "We couldn't locate the client using the provided API key. Please verify it before trying again."
        NOT_FOUND_FOR_UPDATE = "The requested client was not found, so we couldn't update their status."
        UPDATE_STATUS_FAILED = "An error occurred while updating the client's status. Please try again later."
        GET_ALL_FAILED = "We were unable to load the list of clients. Please try again later."
        NOT_FOUND_FOR_DELETE = "The specified client was not found, so deletion could not be completed."
        DELETE_FAILED = "An error occurred while deleting the client. Please try again later."
        NOT_FOUND = "Client not found for the given client ID."
        GET_BY_NAME_FAILED = "We couldn't retrieve the client details using the provided name. Please check and try again."

    class Channel(str, Enum):
        CREATE_FAILED = "We were unable to create a new channel at this time. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve the channel details. Please verify the channel ID and try again."
        GET_BY_NAME_FAILED = "We couldn't retrieve channel details using the provided name. Please check and try again."
        UPDATE_STATUS_FAILED = "An error occurred while updating the channel status. Please try again later."
        NOT_FOUND_FOR_UPDATE = "The requested channel was not found. Status update cannot be performed."
        GET_ALL_FAILED = "We were unable to load the list of channels. Please try again later."
        DELETE_FAILED = "An error occurred while deleting the channel. Please try again later."
        NOT_FOUND_FOR_DELETE = "The specified channel was not found, so deletion could not be completed."
        NOT_FOUND = "Channel not found for the given channel ID."

    class Provider(str, Enum):
        CREATE_FAILED = "We were unable to create a new provider at this time. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve the provider details. Please verify the provider ID and try again."
        GET_BY_CHANNEL_ID_FAILED = "We couldn't retrieve providers for the specified channel. Please check the channel ID and try again."
        UPDATE_STATUS_FAILED = "An error occurred while updating the provider status. Please try again later."
        NOT_FOUND_FOR_UPDATE = "The specified provider was not found, so status update could not be performed."
        GET_ALL_FAILED = "We were unable to load the list of providers. Please try again later."
        DELETE_FAILED = "An error occurred while deleting the provider. Please try again later."
        NOT_FOUND_FOR_DELETE = "The specified provider was not found, so deletion could not be completed."
        NOT_FOUND = "Provider not found for the given provider ID."

    class Receiver(str, Enum):
        CREATE_FAILED = "We were unable to create a new receiver at this time. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve receiver details. Please verify the receiver ID and try again."
        GET_BY_CLIENT_ID_FAILED = "We couldn't retrieve receivers for the specified client. Please check the client ID and try again."
        DELETE_FAILED = "An error occurred while deleting the receiver. Please try again later."
        NOT_FOUND_FOR_DELETE = "The specified receiver was not found, so deletion could not be completed."
        NOT_FOUND = "Receiver not found for the given receiver ID."
        NOT_FOUND_FOR_CLIENT_ID = "Receiver not found for the given client ID."

    class Template(str, Enum):
        CREATE_FAILED = "We were unable to create a new template at this time. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve template details. Please verify the template ID and try again."
        GET_ALL_FAILED = "We were unable to load the list of templates. Please try again later."
        GET_BY_PROVIDER_ID_FAILED = "We couldn't retrieve templates for the specified provider. Please check the provider ID and try again."
        GET_BY_CHANNEL_ID_FAILED = "We couldn't retrieve templates for the specified channel. Please check the channel ID and try again."
        DELETE_FAILED = "An error occurred while deleting the template. Please try again later."
        NOT_FOUND_FOR_DELETE = "The specified template was not found, so deletion could not be completed."
        NOT_FOUND = "Template not found for the given template ID."
        UPDATE_FAILED = "An error occurred while updating the template. Please try again later."

    class Request(str, Enum):
        CREATE_FAILED = "We were unable to create a new request at this time. Please try again later."
        GET_BY_ID_FAILED = "We couldn't retrieve the request details. Please verify the request ID and try again."
        GET_BY_RECEIVER_FAILED = "We couldn't retrieve requests for the specified receiver. Please check the receiver ID and try again."
        STATUS_UPDATE_FAILED = "An error occurred while updating the request status. Please try again later."
        NOT_FOUND = "Request not found for the given request ID."
