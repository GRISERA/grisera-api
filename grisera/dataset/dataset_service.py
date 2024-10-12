from typing import Union, List

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

    def get_datasets(self, dataset_ids: List[Union[int, str]]):
        """
        Get all datasets that you have access to

        Args:
            dataset_ids (List[Union[int, str]]): identity of datasets

        Returns:
            Result of request as list of dataset objects
        """
        raise Exception("get_datasets not implemented yet")

    def get_dataset(self, dataset_id: Union[int, str]):
        """
        Get dataset by id

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

    def update_dataset(self, dataset_id: Union[int, str], dataset: DatasetIn):
        """
        Send request to grisera api to update given dataset
        Args:
            dataset_id (int | str): identity of dataset
            dataset (DatasetIn): Dataset with new values to update
        Returns:
            Result of request as dataset object
        """
        raise Exception("update_dataset not implemented yet")
