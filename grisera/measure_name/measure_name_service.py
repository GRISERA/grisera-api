from typing import Union

from grisera.measure_name.measure_name_model import MeasureNameIn


class MeasureNameService:
    """
    Abstract class to handle logic of measure name requests

    """

    def save_measure_name(self, measure_name: MeasureNameIn):
        """
        Send request to graph api to create new measure name

        Args:
            measure_name (MeasureNameIn): Measure name to be added

        Returns:
            Result of request as measure name object
        """

        raise Exception("save_measure_name not implemented yet")

    def get_measure_names(self):
        """
        Send request to graph api to get all measure names

        Returns:
            Result of request as list of measure name objects
        """
        raise Exception("get_measure_names not implemented yet")

    def get_measure_name(self, measure_name_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given measure name

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_name_id (int | str): Id of measure name

        Returns:
            Result of request as measure name object
        """
        raise Exception("get_measure_name not implemented yet")
