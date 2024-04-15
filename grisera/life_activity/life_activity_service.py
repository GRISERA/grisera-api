from typing import Union

from grisera.life_activity.life_activity_model import LifeActivityIn


class LifeActivityService:
    """
    Abstract class to handle logic of life activity requests

    """

    def save_life_activity(self, life_activity: LifeActivityIn):
        """
        Send request to graph api to create new life activity

        Args:
            life_activity (LifeActivityIn): Life activity to be added

        Returns:
            Result of request as life activity object
        """
        raise Exception("save_life_activity not implemented yet")

    def get_life_activities(self):
        """
        Send request to graph api to get all life activities

        Returns:
            Result of request as list of life activity objects
        """
        raise Exception("get_life_activities not implemented yet")

    def get_life_activity(self, life_activity_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given life activity

        Args:
            life_activity_id (int | str): identity of life activity
            depth: (int): specifies how many related entities will be traversed to create the response

        Returns:
            Result of request as life activity object
        """
        raise Exception("get_life_activity not implemented yet")
