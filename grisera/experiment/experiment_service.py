from typing import Union

from grisera.experiment.experiment_model import ExperimentIn


class ExperimentService:
    """
    Abstract class to handle logic of experiments requests

    """

    def save_experiment(self, experiment: ExperimentIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new experiment

        Args:
            experiment (ExperimentIn): Experiment to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("save_experiment not implemented yet")

    def get_experiments(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get experiments

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of experiments objects
        """
        raise Exception("get_experiments not implemented yet")

    def get_experiment(self, experiment_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given experiment

        Args:
            experiment_id (int | str): identity of experiment
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("get_experiment not implemented yet")

    def delete_experiment(self, experiment_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given experiment

        Args:
            experiment_id (int | str): identity of experiment
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("delete_experiment not implemented yet")

    def update_experiment(self, experiment_id: Union[int, str], experiment: ExperimentIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given experiment

        Args:
            experiment_id (int | str): identity of experiment
            experiment (ExperimentIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("update_experiment not implemented yet")
