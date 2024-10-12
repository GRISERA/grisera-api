from typing import Union

from grisera.activity.activity_model import ActivityIn


class ActivityService:
    """
    Abstract class to handle logic of activity requests

    """

    def save_activity(self, activity: ActivityIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def get_activities(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get all activities

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of activity objects
        """
        raise Exception("Reference to an abstract class.")

    def get_activity(self, activity_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given activity
        Args:
            depth (int): specifies how many related entities will be traversed to create the response
            activity_id (int | str): identity of activity
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def delete_activity(self, activity_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given activity
        Args:
            activity_id (int | str): ID of activity
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity(self, activity_id: Union[int, str], activity: ActivityIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given activity
        Args:
            activity_id (int | str): ID of activity
            activity (ActivityIn): Activity to be updated
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")
