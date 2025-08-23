from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class ParameterType(str, Enum):
    """
    Types of additional parameters
    
    Attributes:
        participant (str): Parameter for participants
        activity (str): Parameter for activities
        participant_state (str): Parameter for participant states
        activity_execution (str): Parameter for activity executions
    """
    
    participant = "participant"
    activity = "activity"
    participant_state = "participantState"
    activity_execution = "activityExecution"


class AdditionalParameterIn(BaseModel):
    """
    Model of additional parameter to acquire from client
    
    Attributes:
        name (str): Name of the parameter
        key (Optional[str]): Key identifier for the parameter
        type (ParameterType): Type of parameter (participant, activity, etc.)
        options (Optional[List[str]]): Available options for the parameter
    """
    
    name: str
    key: Optional[str]
    type: ParameterType
    options: Optional[List[str]] = []


class BasicAdditionalParameterOut(AdditionalParameterIn):
    """
    Basic model of additional parameter to send to client as a result of request
    
    Attributes:
        id (Optional[int | str]): Id of parameter returned from api
        dataset_id (Optional[int | str]): Id of dataset this parameter belongs to
    """
    
    id: Optional[Union[int, str]]
    dataset_id: Optional[Union[int, str]]


class AdditionalParameterOut(BasicAdditionalParameterOut, BaseModelOut):
    """
    Model of additional parameter with relationships to send to client as a result of request
    """
    pass


class AdditionalParametersOut(BaseModelOut):
    """
    Model of additional parameters to send to client as a result of request
    
    Attributes:
        parameters (List[BasicAdditionalParameterOut]): Parameters from database
    """
    
    parameters: List[BasicAdditionalParameterOut] = []