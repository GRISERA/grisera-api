from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut
from grisera.property.property_model import PropertyIn


class Activity(str, Enum):
    """
    The type of activity

    Attributes:
    individual (str): Individual activity
    two_people (str): Two people activity
    group (str): Group activity

    """

    individual = "individual"
    two_people = "two-people"
    group = "group"


class ActivityPropertyIn(BaseModel):
    """
        Model of activity execution to acquire from client

        Attributes:
        activity (str): Type of activity
        additional_properties (Optional[List[PropertyIn]]): Additional properties for activity
        """

    activity: str
    additional_properties: Optional[List[PropertyIn]]


class ActivityIn(ActivityPropertyIn):
    """
    Model of activity

    """


class BasicActivityOut(ActivityIn):
    """
    Model of activity in database

    Attributes:
    id (Optional[Union[int, str]]): identity of activity returned from api
    """

    id: Optional[Union[int, str]]


class ActivityOut(BasicActivityOut, BaseModelOut):
    """
    Model of activity to send to client as a result of request

    Attributes:
    activity_executions (Optional[List[ActivityExecutionOut]]): activity_executions related to this activity
    """

    activity_executions: "Optional[List[ActivityExecutionOut]]"


class ActivitiesOut(BaseModelOut):
    """
    Model of activities to send to client as a result of request

    Attributes:
    activity_types (List[BasicActivityOut]): Activity types from database
    """

    activities: List[BasicActivityOut] = []


# Circular import exception prevention
from grisera.activity_execution.activity_execution_model import ActivityExecutionOut

ActivityOut.update_forward_refs()
