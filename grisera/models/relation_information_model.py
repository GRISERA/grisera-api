from pydantic import BaseModel
from typing import Union


class RelationInformation(BaseModel):
    """
    Simplified model of relation, which passes information

    Attributes:
        second_node_id (int | str): ID of second node of relation. It can be start node or end node.
        relation_id (int | str): ID of relationship from database.
        name (str): Name of relationship.
    """
    second_node_id: Union[int, str]
    relation_id: Union[int, str]
    name: str
