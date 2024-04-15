from typing import Union

from grisera.participant.participant_model import ParticipantIn


class ParticipantService:
    """
    Abstract class to handle logic of participants requests

    """

    def save_participant(self, participant: ParticipantIn):
        """
        Send request to graph api to create new participant

        Args:
            participant (ParticipantIn): Participant to be added

        Returns:
            Result of request as participant object
        """
        raise Exception("save_participant not implemented yet")

    def get_participants(self):
        """
        Send request to graph api to get participants

        Returns:
            Result of request as list of participants objects
        """
        raise Exception("get_participants not implemented yet")

    def get_participant(self, participant_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participant

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participant_id (int | str): identity of participant

        Returns:
            Result of request as participant object
        """
        raise Exception("get_participant not implemented yet")

    def delete_participant(self, participant_id: Union[int, str]):
        """
        Send request to graph api to delete given participant

        Args:
            participant_id (int | str): identity of participant

        Returns:
            Result of request as participant object
        """
        raise Exception("delete_participant not implemented yet")

    def update_participant(self, participant_id: Union[int, str], participant: ParticipantIn):
        """
        Send request to graph api to update given participant

        Args:
            participant_id (int | str): identity of participant
            participant (ParticipantIn): Properties to update

        Returns:
            Result of request as participant object
        """
        raise Exception("update_participant not implemented yet")
