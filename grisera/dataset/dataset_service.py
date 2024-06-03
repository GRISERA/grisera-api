from typing import Union

from grisera.dataset.dataset_model import DatasetIn


class DatasetService:
    def save_dataset(self, dataset: DatasetIn):
        """
        Creates new dataset

        Args:
            dataset (DatasetIn): Dataset to be added

        Returns:
            Result of request as dataset object
        """

        raise Exception("save_database not implemented yet")

    def get_datasets(self):
        """
        Get all datasets

        Returns:
            Result of request as list of dataset objects
        """
        raise Exception("get_datasets not implemented yet")

    def get_dataset(self, dataset_id: Union[int, str]):
        """
        Get dataset by name

        Args:
            dataset_id (int | str): identity of dataset

        Returns:
            Result of request as dataset object
        """
        raise Exception("get_dataset not implemented yet")

    def delete_dataset(self, dataset_id: Union[int, str]):
        """
        Delete given dataset

        Args:
            dataset_id (int | str): identity of dataset

        Returns:
            Result of request as dataset object
        """
        raise Exception("delete_dataset not implemented yet")
