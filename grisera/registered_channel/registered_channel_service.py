from typing import Union

from grisera.registered_channel.registered_channel_model import RegisteredChannelIn


class RegisteredChannelService:
    """
    Abstract class to handle logic of registered channels requests

    """

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to create new registered channel

        Args:
            registered_channel (RegisteredChannelIn): Registered channel to be added

        Returns:
            Result of request as registered channel object
        """
        raise Exception("save_registered_channel not implemented yet")

    def get_registered_channels(self):
        """
        Send request to graph api to get registered channels

        Returns:
            Result of request as list of registered channels objects
        """
        raise Exception("get_registered_channels not implemented yet")

    def get_registered_channel(self, registered_channel_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given registered channel

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            registered_channel_id (int | str): identity of registered channel

        Returns:
            Result of request as registered channel object
        """
        raise Exception("get_registered_channel not implemented yet")

    def delete_registered_channel(self, registered_channel_id: Union[int, str]):
        """
        Send request to graph api to delete given registered channel

        Args:
            registered_channel_id (int | str): identity of registered channel

        Returns:
            Result of request as registered channel object
        """
        raise Exception("delete_registered_channel not implemented yet")

    def update_registered_channel_relationships(self, registered_channel_id: Union[int, str],
                                                registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to update given registered channel

        Args:
            registered_channel_id (int | str): identity of registered channel
            registered_channel (RegisteredChannelIn): Relationships to update

        Returns:
            Result of request as registered channel object
        """
        raise Exception("update_registered_channel_relationships not implemented yet")
