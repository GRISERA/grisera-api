from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class LifeActivity(str, Enum):
    """
    Actions of a human body

    Attributes:
    movement (str): Movement
    sound (str): Sound
    heart_activity (str): Heart activity
    muscles_activity (str): Muscles activity
    perspiration (str): Perspiration
    respiration (str): Respiration
    thermal_regulation (str): Thermal regulation
    brain_activity (str): Brain activity
    """

    movement = "movement"
    sound = "sound"
    heart_activity = "heart activity"
    muscles_activity = "muscles activity"
    perspiration = "perspiration"
    respiration = "respiration"
    thermal_regulation = "thermal regulation"
    brain_activity = "brain activity"


class LifeActivityIn(BaseModel):
    """
    Model of actions of a human body observed during experiment

    Attributes:
    life_activity (str): Actions of a human body
    """

    life_activity: str


class BasicLifeActivityOut(LifeActivityIn):
    """
    Model of actions of a human body during experiment in database

    Attributes:
    id (Optional[Union[int, str]]): Id of node returned from api
    """

    id: Optional[Union[int, str]]


class LifeActivityOut(BasicLifeActivityOut, BaseModelOut):
    """
    Model of actions of a human body during experiment to send to client as a result of request

    Attributes:
    observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
        this life activity
    """

    observable_informations: "Optional[List[ObservableInformationOut]]"


class LifeActivitiesOut(BaseModelOut):
    """
    Model of actions of a human body during experiment to send to client as a result of request

    Attributes:
    life_activities (List[BasicLifeActivityOut]): Life activities from database
    """

    life_activities: List[BasicLifeActivityOut] = []


# Circular import exception prevention
from grisera.observable_information.observable_information_model import ObservableInformationOut

LifeActivityOut.update_forward_refs()
