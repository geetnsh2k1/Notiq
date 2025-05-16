from models.receiver import Receiver
from schema.receiver import ReceiverCreate, ReceiverDetails

class ReceiverMapper:
    @staticmethod
    def receiver_create_to_model(receiver_create: ReceiverCreate) -> Receiver:
        """
        Converts a ReceiverCreate DTO to a Receiver model instance.

        Args:
            receiver_create (ReceiverCreate): The DTO containing receiver creation data.

        Returns:
            Receiver: The Receiver model instance.
        """
        return Receiver(
            client_id=receiver_create.client_id,
            user_id=receiver_create.user_id,
            email=receiver_create.email,
            phone_number=receiver_create.phone_number,
            meta_data=receiver_create.meta_data,
        )

    @staticmethod
    def model_to_receiver_response(receiver: Receiver) -> ReceiverDetails:
        """
        Converts a Receiver model instance to a ReceiverDetails DTO.

        Args:
            receiver (Receiver): The Receiver model instance.

        Returns:
            ReceiverDetails: The DTO containing receiver details.
        """
        return ReceiverDetails(
            id=receiver.id,
            client_id=receiver.client_id,
            user_id=receiver.user_id,
            email=receiver.email,
            phone_number=receiver.phone_number,
            meta_data=receiver.meta_data,
        )