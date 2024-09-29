from typing import Union

from grisera.participation.participation_model import ParticipationIn


class ParticipationService:
    """
    Abstract class to handle logic of participation requests

    """

    def save_participation(self, participation: ParticipationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new participation

        Args:
            participation (ParticipationIn): Participation to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as participation object
        """
        raise Exception("save_participation not implemented yet")

    def get_participations(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get participations

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of participation objects
        """
        raise Exception("get_participations not implemented yet")

    def get_participation(self, participation_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participation
        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participation_id (int | str): identity of participation
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as participation object
        """
        raise Exception("get_participation not implemented yet")

    def delete_participation(self, participation_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given participation
        Args:
            participation_id (int | str): identity of participation
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as participation object
        """
        raise Exception("delete_participation not implemented yet")

    def update_participation_relationships(self, participation_id: Union[int, str],
                                           participation: ParticipationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given participation relationships
        Args:
            participation_id (int | str): identity of participation
            participation (ParticipationIn): Relationships to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as participation object
        """
        raise Exception("update_participation_relationships not implemented yet")
