from typing import Union

from grisera.arrangement.arrangement_model import ArrangementIn


class ArrangementService:
    """
    Abstract class to handle logic of arrangement requests

    """

    def save_arrangement(self, arrangement: ArrangementIn, dataset_name: str):
        """
        Send request to graph api to create new arrangement

        Args:
            arrangement (ArrangementIn): Arrangement to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as arrangement object
        """
        raise Exception("save_arrangement not implemented yet")

    def get_arrangements(self, dataset_name: str):
        """
        Send request to graph api to get all arrangements

        Args:
            dataset_name (str): name of dataset
        Returns:
            Result of request as list of arrangement objects
        """
        raise Exception("get_arrangements not implemented yet")

    def get_arrangement(self, arrangement_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given arrangement

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            arrangement_id (int | str): identity of arrangement
            dataset_name (str): name of dataset

        Returns:
            Result of request as arrangement object
        """
        raise Exception("get_arrangement not implemented yet")

    def delete_arrangement(self, arrangement_id: int, dataset_name: str):
        """
        Send request to graph api to delete given arrangement
        Args:
            arrangement_id (int): Id of arrangement
            dataset_name (str): name of dataset
        Returns:
            Result of request as arrangement object
        """
        raise Exception("Reference to an abstract class.")

    def update_arrangement(self, arrangement_id: int, arrangement: ArrangementIn, dataset_name: str):
        """
        Send request to graph api to update given arrangement
        Args:
            arrangement_id (int): Id of arrangement
            arrangement (ArrangementIn): Arrangement to be updated
            dataset_name (str): name of dataset
        Returns:
            Result of request as arrangement object
        """
        raise Exception("Reference to an abstract class.")
