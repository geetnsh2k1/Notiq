from models.provider import Provider
from schema.provider import ProviderCreate, ProviderDetails


class ProviderMapper:
    @staticmethod
    def provider_create_to_model(
        provider_create: ProviderCreate,
    ) -> Provider:
        """
        Converts a ProviderCreate object fields to a Provider model.
        """
        return Provider(
            name=provider_create.name.lower(),
            channel_id=provider_create.channel_id,
            config=provider_create.config,
            is_active=True,
        )

    @staticmethod
    def model_to_provider_response(provider: Provider) -> ProviderDetails:
        """
        Converts a Provider model to a ProviderDetails object.
        """
        return ProviderDetails(
            id=provider.id,
            name=provider.name,
            channel_id=provider.channel_id,
            config=provider.config,
            is_active=provider.is_active,
        )