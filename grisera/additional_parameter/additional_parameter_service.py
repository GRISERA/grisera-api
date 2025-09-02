from typing import Union

from grisera.additional_parameter.additional_parameter_model import AdditionalParameterIn


class AdditionalParameterService:
    """
    Abstract class to handle logic of additional parameters requests

    """

    def save_additional_parameter(self, parameter: AdditionalParameterIn, dataset_id: Union[int, str]):
        """
        Send request to database to create new additional parameter

        Args:
            parameter (AdditionalParameterIn): Additional parameter to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as additional parameter object
        """
        raise Exception("save_additional_parameter not implemented yet")

    def get_additional_parameters(self, dataset_id: Union[int, str]):
        """
        Send request to database to get additional parameters

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of additional parameters objects
        """
        raise Exception("get_additional_parameters not implemented yet")

    def get_additional_parameter(self, parameter_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to database to get given additional parameter

        Args:
            parameter_id (int | str): identity of additional parameter
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as additional parameter object
        """
        raise Exception("get_additional_parameter not implemented yet")

    def delete_additional_parameter(self, parameter_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to database to delete given additional parameter

        Args:
            parameter_id (int | str): identity of additional parameter
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as additional parameter object
        """
        raise Exception("delete_additional_parameter not implemented yet")

    def update_additional_parameter(self, parameter_id: Union[int, str], parameter: AdditionalParameterIn, dataset_id: Union[int, str]):
        """
        Send request to database to update given additional parameter

        Args:
            parameter_id (int | str): identity of additional parameter
            parameter (AdditionalParameterIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as additional parameter object
        """
        raise Exception("update_additional_parameter not implemented yet")

    def get_additional_parameters_by_dataset(self, dataset_id: Union[int, str]):
        """
        Send request to database to get additional parameters for given dataset

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of additional parameters objects
        """
        raise Exception("get_additional_parameters_by_dataset not implemented yet")