from typing import Union

from grisera.recording.recording_model import RecordingPropertyIn, RecordingIn, RecordingRelationIn


class RecordingService:
    """
    Abstract class to handle logic of recording requests

    """

    def save_recording(self, recording: RecordingIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new recording node

        Args:
            recording (RecordingIn): Recording to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as recording object
        """
        raise Exception("save_recording not implemented yet")

    def get_recordings(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get recordings

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of recordings objects
        """
        raise Exception("get_recordings not implemented yet")

    def get_recording(self, recording_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given recording
        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            recording_id (int | str): identity of recording
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as recording object
        """
        raise Exception("get_recording not implemented yet")

    def delete_recording(self, recording_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given recording
        Args:
            recording_id (int | str): identity of recording
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as recording object
        """
        raise Exception("delete_recording not implemented yet")

    def update_recording(self, recording_id: Union[int, str], recording: RecordingPropertyIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given participant state
        Args:
            recording_id (int | str): identity of participant state
            recording (RecordingPropertyIn): Properties to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as participant state object
        """
        raise Exception("update_recording not implemented yet")

    def update_recording_relationships(self, recording_id: Union[int, str],
                                       recording: RecordingRelationIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to update given recording
        Args:
            recording_id (int | str): identity of recording
            recording (RecordingRelationIn): Relationships to update
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as recording object
        """
        raise Exception("update_recording_relationships not implemented yet")
