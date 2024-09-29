from typing import Union

from grisera.appearance.appearance_model import AppearanceOcclusionIn, AppearanceSomatotypeIn


class AppearanceService:
    """
    Abstract class to handle logic of appearance requests

    """

    def save_appearance_occlusion(self, appearance: AppearanceOcclusionIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new appearance occlusion model

        Args:
            appearance (AppearanceIn): Appearance to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance state object
        """
        raise Exception("save_appearance_occlusion not implemented yet")

    def save_appearance_somatotype(self, appearance: AppearanceSomatotypeIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new appearance somatotype model

        Args:
            appearance (AppearanceIn): Appearance to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance state object
        """
        raise Exception("save_appearance_somatotype not implemented yet")

    def get_appearance(self, appearance_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given appearance

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            appearance_id (int | str): identity of appearance
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance object
        """
        raise Exception("get_appearance not implemented yet")

    def get_appearances(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get appearances

        Args:
            dataset_id (int | str): name of dataset
        Returns:
            Result of request as list of appearances objects
        """
        raise Exception("get_appearances not implemented yet")

    def delete_appearance(self, appearance_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given appearance

        Args:
            appearance_id (int | str): identity of appearance
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance object
        """
        raise Exception("delete_appearance not implemented yet")

    def update_appearance_occlusion(self, appearance_id: Union[int, str], appearance: AppearanceOcclusionIn,
                                    dataset_id: Union[int, str]):
        """
        Send request to graph api to update given appearance occlusion model

        Args:
            appearance_id (int | str): identity of appearance
            appearance (AppearanceOcclusionIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance object
        """
        raise Exception("update_appearance_occlusion not implemented yet")

    def update_appearance_somatotype(self, appearance_id: Union[int, str], appearance: AppearanceSomatotypeIn,
                                     dataset_id: Union[int, str]):
        """
        Send request to graph api to update given appearance somatotype model

        Args:
            appearance_id (int | str): identity of appearance
            appearance (AppearanceSomatotypeIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as appearance object
        """
        raise Exception("update_appearance_somatotype not implemented yet")
