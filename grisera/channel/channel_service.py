from typing import Union

from grisera.channel.channel_model import ChannelIn


class ChannelService:
    """
    Abstract class to handle logic of channel requests

    """

    def save_channel(self, channel: ChannelIn):
        """
        Send request to graph api to create new channel

        Args:
            channel (ChannelIn): Channel to be added

        Returns:
            Result of request as channel object
        """
        raise Exception("save_channel not implemented yet")

    def get_channels(self):
        """
        Send request to graph api to get all channels

        Returns:
            Result of request as list of channel objects
        """
        raise Exception("get_channels not implemented yet")

    def get_channel(self, channel_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given channel

        Args:
            channel_id (int | str ): identity of channel
            depth: (int): specifies how many related entities will be traversed to create the response

        Returns:
            Result of request as channel object
        """
        raise Exception("get_channel not implemented yet")
