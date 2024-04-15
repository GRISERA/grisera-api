from typing import Union

from grisera.modality.modality_model import ModalityIn


class ModalityService:
    """
    Abstract class to handle logic of modality requests

    """

    def save_modality(self, modality: ModalityIn):
        """
        Send request to graph api to create new modality

        Args:
            modality (ModalityIn): Modality to be added

        Returns:
            Result of request as modality object
        """
        raise Exception("save_modality not implemented yet")

    def get_modalities(self):
        """
        Send request to graph api to get all modalities

        Returns:
            Result of request as list of modality objects
        """
        raise Exception("get_modalities not implemented yet")

    def get_modality(self, modality_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given modality

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            modality_id (int | str): identity of modality

        Returns:
            Result of request as modality object
        """
        raise Exception("get_modality not implemented yet")
