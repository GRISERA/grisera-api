from typing import Union
from grisera.activity.activity_model import ActivityIn


class ActivityService:
    """
    Abstract class to handle logic of activity requests

    """

    def save_activity(self, activity: ActivityIn):
        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def get_activities(self):
        """
        Send request to graph api to get all activities

        Returns:
            Result of request as list of activity objects
        """
        raise Exception("Reference to an abstract class.")

    def get_activity(self, activity_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given activity
        Args:
            depth (int): specifies how many related entities will be traversed to create the response
            activity_id (int | str): identity of activity
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")
