from typing import Optional, List, Union

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut
from grisera.property.property_model import PropertyIn


class ActivityExecutionPropertyIn(BaseModel):
    """
    Model of activity execution to acquire from client

    Attributes:
    additional_properties (Optional[List[PropertyIn]]): Additional properties for activity execution
    """

    additional_properties: Optional[List[PropertyIn]]


class ActivityExecutionRelationIn(BaseModel):
    """
    Model of activity execution relations to acquire from client

    Attributes:
    activity_id (int | str): identity of activity
    arrangement_id (int | str) : identity number of arrangement
    """

    activity_id: Optional[Union[int, str]]
    arrangement_id: Optional[Union[int, str]]


class ActivityExecutionIn(ActivityExecutionPropertyIn, ActivityExecutionRelationIn):
    """
    Full model of activity execution to acquire from client

    """


class BasicActivityExecutionOut(ActivityExecutionIn):
    """
    Basic model of activity execution

    Attributes:
    id (Optional[Union[int, str]]): Id of activity execution returned from api
    """

    id: Optional[Union[int, str]]


class ActivityExecutionOut(BasicActivityExecutionOut, BaseModelOut):
    """
    Model of activity execution to send to client as a result of request

    Attributes:
    activity (Optional[ActivityOut]): activity related to this activity execution
    participations (Optional[List[ParticipationOut]]): participations related to this activity execution
    experiments (Optional[List[ExperimentOut]]): experiments related to this activity execution
    arrangements (Optional[ArrangementOut]): arrangements related to this activity execution
    """

    activity: "Optional[ActivityOut]"
    participations: "Optional[List[ParticipationOut]]"
    experiments: "Optional[List[ExperimentOut]]"
    arrangement: "Optional[ArrangementOut]"


class ActivityExecutionsOut(BaseModelOut):
    """
    Model of activity executions to send to client as a result of request

    Attributes:
    activity_executions (List[BasicActivityExecutionOut]): Activity executions from database
    """

    activity_executions: List[BasicActivityExecutionOut] = []


# Circular import exception prevention
from grisera.participation.participation_model import ParticipationOut
from grisera.activity.activity_model import ActivityOut
from grisera.experiment.experiment_model import ExperimentOut
from grisera.arrangement.arrangement_model import ArrangementOut

ActivityExecutionOut.update_forward_refs()
