from typing import Union

from grisera.arrangement.arrangement_model import ArrangementIn


class ArrangementService:
    """
    Abstract class to handle logic of arrangement requests

    """

    def save_arrangement(self, arrangement: ArrangementIn):
        """
        Send request to graph api to create new arrangement

        Args:
            arrangement (ArrangementIn): Arrangement to be added

        Returns:
            Result of request as arrangement object
        """
        raise Exception("save_arrangement not implemented yet")

    def get_arrangements(self):
        """
        Send request to graph api to get all arrangements

        Returns:
            Result of request as list of arrangement objects
        """
        raise Exception("get_arrangements not implemented yet")

    def get_arrangement(self, arrangement_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given arrangement

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            arrangement_id (int | str): identity of arrangement

        Returns:
            Result of request as arrangement object
        """
        raise Exception("get_arrangement not implemented yet")
