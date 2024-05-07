from grisera.dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.models.relation_information_model import RelationInformation


class DatasetService:
    def save_dataset(self, dataset_name: str):
        """
        Creates new dataset

        Args:
            dataset_name (str): name of dataset to create

        Returns:
            Result of request as dataset object
        """

        raise Exception("save_database not implemented yet")

    def get_datasets(self, dataset_name: str):
        """
        Get all datasets

        Returns:
            Result of request as list of dataset objects
        """
        raise Exception("get_datasets not implemented yet")
    
    def get_dataset(self, dataset_name: str):
        """
        Get dataset by name

        Args:
            dataset_name (str): name of dataset

        Returns:
            Result of request as dataset object
        """
        raise Exception("get_dataset not implemented yet")
    
    def delete_dataset(self, dataset_name: str):
        """
        Delete given dataset

        Args:
            dataset_name (str): name of dataset

        Returns:
            Result of request as dataset object
        """
        raise Exception("delete_dataset not implemented yet")
