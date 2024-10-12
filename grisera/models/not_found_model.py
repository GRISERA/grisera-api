from typing import Optional, Any, Union

from pydantic import BaseModel


class NotFoundByIdModel(BaseModel):
    """
    Model send when source was not found by id

    Attributes:
        id (int | str): Id of searching source
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Union[int, str] = None
    errors: Optional[Any] = None
    links: Optional[list] = None
