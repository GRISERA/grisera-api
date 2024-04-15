from typing import Union

from grisera.participant_state.participant_state_model import ParticipantStatePropertyIn, ParticipantStateIn, \
    ParticipantStateRelationIn


class ParticipantStateService:
    """
    Abstract class to handle logic of participant state requests

    """

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        raise Exception("save_participant_state not implemented yet")

    def get_participant_states(self):
        """
        Send request to graph api to get participant states

        Returns:
            Result of request as list of participant states objects
        """
        raise Exception("get_participant_states not implemented yet")

    def get_participant_state(self, participant_state_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participant state

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participant_state_id (int | str): identity of participant state

        Returns:
            Result of request as participant state object
        """
        raise Exception("get_participant_state not implemented yet")

    def delete_participant_state(self, participant_state_id: Union[int, str]):
        """
        Send request to graph api to delete given participant state

        Args:
            participant_state_id (int | str): identity of participant state

        Returns:
            Result of request as participant state object
        """
        raise Exception("delete_participant_state not implemented yet")

    def update_participant_state(self, participant_state_id: Union[int, str],
                                 participant_state: ParticipantStatePropertyIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int | str): identity of participant state
            participant_state (ParticipantStatePropertyIn): Properties to update

        Returns:
            Result of request as participant state object
        """
        raise Exception("update_participant_state not implemented yet")

    def update_participant_state_relationships(self, participant_state_id: Union[int, str],
                                               participant_state: ParticipantStateRelationIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int | str): identity of participant state
            participant_state (ParticipantStateRelationIn): Relationships to update

        Returns:
            Result of request as participant state object
        """
        raise Exception("update_participant_state_relationships not implemented yet")
