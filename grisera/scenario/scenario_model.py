from typing import Union, List, Optional

from pydantic import BaseModel

from grisera.activity_execution.activity_execution_model import ActivityExecutionIn
from grisera.models.base_model_out import BaseModelOut


class ScenarioIn(BaseModel):
    """
    Model of scenario to acquire from client

    Attributes:
    activity_executions (List[ActivityExecutionIn]): list of activity executions in scenario
    """

    experiment_id: Optional[Union[int, str]]
    activity_executions: Optional[List[ActivityExecutionIn]]


class ScenarioOut(BaseModelOut):
    """
    Model of scenario to send to client as a result of request

    Attributes:
        id (Union[int, str]): Id of scenario returned from api
        activity_executions (List[ActivityExecutionOut]): List of activity executions in scenario
        experiment (ExperimentOut): Experiment, the scenario belongs to
    """

    id: Optional[Union[int, str]]
    activity_executions: "Optional[List[ActivityExecutionOut]]"
    experiment: "Optional[ExperimentOut]"


class OrderChangeIn(BaseModel):
    """
    Model of ids to change order in scenario

    Attributes:
    previous_id (Union[int, str]): Id of activity execution/experiment to put activity execution after that
    activity_execution_id (Union[int, str]): Id of activity execution to change order of it
    """

    previous_id: Union[int, str]
    activity_execution_id: Union[int, str]


class OrderChangeOut(BaseModelOut):
    """
    Model of changed order in scenario
    """


# Circular import exception prevention
from grisera.activity_execution.activity_execution_model import ActivityExecutionOut
from grisera.experiment.experiment_model import ExperimentOut

ScenarioOut.update_forward_refs()
