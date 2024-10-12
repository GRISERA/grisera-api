from typing import Union

from pydantic import BaseModel


class PropertyIn(BaseModel):
    """
    Model of property to acquire from client

    Attributes:
        key (str): Key of property added to node or relationship
        value (Union[str, int]): Value of property added to node or relationship
    """
    key: str
    value: Union[str, int]
