from typing import Union

from grisera.measure_name.measure_name_model import MeasureNameIn


class MeasureNameService:
    """
    Abstract class to handle logic of measure name requests

    """

    def save_measure_name(self, measure_name: MeasureNameIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new measure name

        Args:
            measure_name (MeasureNameIn): Measure name to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure name object
        """

        raise Exception("save_measure_name not implemented yet")

    def get_measure_names(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get all measure names

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of measure name objects
        """
        raise Exception("get_measure_names not implemented yet")

    def get_measure_name(self, measure_name_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given measure name

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_name_id (int | str): ID of measure name
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure name object
        """
        raise Exception("get_measure_name not implemented yet")

    def delete_measure_name(self, measure_name_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given measure_name
        Args:
            measure_name_id (int | str): ID of measure_name
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as measure_name object
        """
        raise Exception("Reference to an abstract class.")

    def update_measure_name(self, measure_name_id: Union[int, str], measure_name: MeasureNameIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given measure_name
        Args:
            measure_name_id (int | str): ID of measure_name
            measure_name (MeasureNameIn): Measure_name to be updated
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as measure_name object
        """
        raise Exception("Reference to an abstract class.")
