from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class Arrangement(tuple, Enum):
    """
    The type of arrangement

    Attributes:
        casual_personal_zone (tuple): Personal two persons arrangement - casual personal zone
        intimate_zone (tuple): Personal two persons arrangement - intimate zone
        public_zone (tuple): Personal two persons arrangement - public zone
        socio_consultive_zone (tuple): Personal two persons arrangement - socio consultive zone
        personal_group (tuple): Personal group arrangement
    """

    casual_personal_zone = ("personal two persons", "casual personal zone")
    intimate_zone = ("personal two persons", "intimate zone")
    public_zone = ("personal two persons", "public zone")
    socio_consultive_zone = ("personal two persons", "socio consultive zone")
    personal_group = ("personal group", None)


class ArrangementIn(BaseModel):
    """
    Model of arrangement

    Attributes:
    arrangement (str): Type of arrangement
    """

    arrangement_type: str
    arrangement_distance: Optional[str]


class BasicArrangementOut(ArrangementIn):
    """
    Model of arrangement in dataset

    Attributes:
    id (Optional[Union[int, str]]): Id of arrangement returned from api
    """

    id: Optional[Union[int, str]]


class ArrangementOut(BasicArrangementOut, BaseModelOut):
    """
    Model of arrangement to send to client as a result of request

    Attributes:
    activity_executions (Optional[ActivityExecutionOut]): activity_executions related to this arrangement
    """

    activity_executions: "Optional[ActivityExecutionOut]"


class ArrangementsOut(BaseModelOut):
    """
    Model of arrangements to send to client as a result of request

    Attributes:

    arrangement_types (List[BasicArrangementOut]): Arrangement types from dataset
    """

    arrangements: List[BasicArrangementOut] = []


# Circular import exception prevention
from grisera.activity_execution.activity_execution_model import ActivityExecutionOut

ArrangementOut.update_forward_refs()
