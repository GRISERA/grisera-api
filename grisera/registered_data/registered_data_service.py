from typing import Union

from grisera.registered_data.registered_data_model import RegisteredDataIn


class RegisteredDataService:
    """
    Abstract class to handle logic of registered data requests

    """

    def save_registered_data(self, registered_data: RegisteredDataIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new registered data node

        Args:
            registered_data (RegisteredDataIn): Registered data to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as registered data object
        """
        raise Exception("save_registered_data not implemented yet")

    def get_registered_data_nodes(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get registered_data_nodes

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of registered_data_nodes objects
        """
        raise Exception("get_registered_data_nodes not implemented yet")

    def get_registered_data(self, registered_data_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given registered data

        Args:
            registered_data_id (int | str): identity of registered data
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as registered data object
        """
        raise Exception("get_registered_data not implemented yet")

    def delete_registered_data(self, registered_data_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given registered data

        Args:
            registered_data_id (int | str): identity of registered data
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as registered data object
        """
        raise Exception("delete_registered_data not implemented yet")

    def update_registered_data(self, registered_data_id: Union[int, str], registered_data: RegisteredDataIn,
                               dataset_id: Union[int, str]):
        """
        Send request to graph api to update given registered data

        Args:
            registered_data_id (int | str): identity of registered data
            registered_data (RegisteredDataIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as registered data object
        """
        raise Exception("update_registered_data not implemented yet")
