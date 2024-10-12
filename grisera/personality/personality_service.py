from typing import Union

from grisera.personality.personality_model import PersonalityBigFiveIn, PersonalityPanasIn


class PersonalityService:
    """
    Abstract class to handle logic of personality requests

    """

    def save_personality_big_five(self, personality: PersonalityBigFiveIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new personality big five model

        Args:
            personality (PersonalityBigFiveIn): Personality big five to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality big five object
        """
        raise Exception("save_personality_big_five not implemented yet")

    def save_personality_panas(self, personality: PersonalityPanasIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to create new personality panas model

        Args:
            personality (PersonalityPanasIn): Personality to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality panas object
        """
        raise Exception("save_personality_panas not implemented yet")

    def get_personality(self, personality_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given personality

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            personality_id (int | str): identity of personality
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality object
        """
        raise Exception("get_personality not implemented yet")

    def get_personalities(self, dataset_id: Union[int, str]):
        """
        Send request to graph api to get personalities

        Args:
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as list of personalities objects
        """
        raise Exception("get_personalities not implemented yet")

    def delete_personality(self, personality_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete given personality

        Args:
            personality_id (int | str): identity of personality
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality object
        """
        raise Exception("delete_personality not implemented yet")

    def update_personality_big_five(self, personality_id: Union[int, str], personality: PersonalityBigFiveIn,
                                    dataset_id: Union[int, str]):
        """
        Send request to graph api to update given personality big five model

        Args:
            personality_id (int | str): identity of personality
            personality (PersonalityBigFiveIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality object
        """
        raise Exception("update_personality_big_five not implemented yet")

    def update_personality_panas(self, personality_id: Union[int, str], personality: PersonalityPanasIn,
                                 dataset_id: Union[int, str]):
        """
        Send request to graph api to update given personality panas model

        Args:
            personality_id (int | str): identity of personality
            personality (PersonalityPanasIn): Properties to update
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as personality object
        """
        raise Exception("update_personality_panas not implemented yet")
