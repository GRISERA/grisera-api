from typing import Union

from grisera.measure.measure_model import MeasurePropertyIn, MeasureIn, MeasureRelationIn


class MeasureService:
    """
    Abstract class to handle logic of measure requests

    """

    def save_measure(self, measure: MeasureIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new measure

        Args:
            measure (MeasureIn): Measure to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure object
        """
        raise Exception("save_measure not implemented yet")

    def get_measures(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get measures

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of measures objects
        """
        raise Exception("get_measures not implemented yet")

    def get_measure(self, measure_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given measure

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_id (int | str): identity of measure
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure object
        """
        raise Exception("get_measure not implemented yet")

    def delete_measure(self, measure_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given measure

        Args:
            measure_id (int | str): identity of measure
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure object
        """
        raise Exception("delete_measure not implemented yet")

    def update_measure(self, measure_id: Union[int, str], measure: MeasurePropertyIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasurePropertyIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure object
        """
        raise Exception("update_measure not implemented yet")

    def update_measure_relationships(self, measure_id: Union[int, str],
                                     measure: MeasureRelationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasureRelationIn): Relationships to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as measure object
        """
        raise Exception("update_measure_relationships not implemented yet")
