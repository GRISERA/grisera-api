from typing import Union


class PermissionService:
    """
    Abstract class to handle logic of permission requests

    """

    def get_permissions(self, user_id: Union[int, str]):
        """
        Send request to API to get permission for a user

        Args:
            user_id (int | str): Identifier of the resource

        Returns:
            Result of request as list of permission objects
        """
        raise Exception("get_permissions not implemented yet")
