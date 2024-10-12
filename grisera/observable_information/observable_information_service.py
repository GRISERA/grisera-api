from typing import Union

from grisera.observable_information.observable_information_model import ObservableInformationIn


class ObservableInformationService:
    """
    Abstract class to handle logic of observable information requests

    """

    def save_observable_information(self, observable_information: ObservableInformationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as observable information object
        """
        raise Exception("save_observable_information not implemented yet")

    def get_observable_informations(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get observable information

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of observable information objects
        """
        raise Exception("get_observable_informations not implemented yet")

    def get_observable_information(self, observable_information_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given observable information
        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            observable_information_id (int | str): identity of observable information
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as observable information object
        """
        raise Exception("get_observable_information not implemented yet")

    def delete_observable_information(self, observable_information_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given observable information
        Args:
            observable_information_id (int | str): identity of observable information
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as observable information object
        """
        raise Exception("delete_observable_information not implemented yet")

    def update_observable_information_relationships(self, observable_information_id: Union[int, str],
                                                    observable_information: ObservableInformationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given observable information
        Args:
            observable_information_id (int | str): identity of observable information
            observable_information (ObservableInformationIn): Relationships to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as observable information object
        """
        raise Exception("update_observable_information_relationships not implemented yet")
