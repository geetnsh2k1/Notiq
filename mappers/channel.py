from models.channel import Channel
from schema.channel import ChannelCreate, ChannelDetails


class ChannelMapper:
    @staticmethod
    def channel_create_to_model(
        channel_create: ChannelCreate,
    ) -> Channel:
        """
        Converts a ChannelCreate object fields to a Channel model.
        """
        return Channel(
            name=channel_create.name.lower(),
            description=channel_create.description,
            is_active=True,
        )

    @staticmethod
    def model_to_channel_response(channel: Channel) -> ChannelDetails:
        """
        Converts a Channel model to a ChannelResponse object.
        """
        return ChannelDetails(
            id=channel.id,
            name=channel.name,
            description=channel.description,
        )