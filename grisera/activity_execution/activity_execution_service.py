from typing import Union

from grisera.activity_execution.activity_execution_model import ActivityExecutionPropertyIn, \
    ActivityExecutionRelationIn, \
    ActivityExecutionIn


class ActivityExecutionService:
    """
    Abstract class to handle logic of activities requests

    """

    def save_activity_execution(self, activity_execution: ActivityExecutionIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity execution to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def get_activity_executions(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get activity executions

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of activity executions objects
        """

        raise Exception("Reference to an abstract class.")

    def get_activity_execution(self, activity_execution_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given activity execution

        Args:
            depth (int): specifies how many related entities will be traversed to create the response
            activity_execution_id (int | str): identity of activity execution
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def delete_activity_execution(self, activity_execution_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given activity execution
        Args:
            activity_execution_id (int | str): identity of activity execution
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution(self, activity_execution_id: Union[int, str],
                                  activity_execution: ActivityExecutionPropertyIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given participant state
        Args:
            activity_execution_id (int | str): identity of activity execution
            activity_execution (ActivityExecutionPropertyIn): Properties to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as participant state object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution_relationships(self, activity_execution_id: Union[int, str],
                                                activity_execution: ActivityExecutionRelationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given activity execution relationships
        Args:
            activity_execution_id (int | str): identity of activity execution
            activity_execution (ActivityExecutionIn): Relationships to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")
