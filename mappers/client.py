from models.client import Client
from schema.client import ClientCreate, ClientDetails
from utils.security import generate_api_key


class ClientMapper:
    @staticmethod
    def client_create_to_model(
        client_name: str,
        hashed_api_key: str,
    ) -> Client:
        """
        Converts a ClientCreate object to a Client model.
        The client_id is passed separately to simulate an auto-generated id,
        such as from a database.
        """
        return Client(
            client_name=client_name,
            api_key=hashed_api_key,
            is_active=True
        )

    @staticmethod
    def model_to_client_details(client: Client) -> ClientDetails:
        """
        Converts a Client object to ClientDetails.
        """
        return ClientDetails(
            id=client.id,
            client_name=client.client_name
        )