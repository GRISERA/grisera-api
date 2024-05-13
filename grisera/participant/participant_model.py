from datetime import date
from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut
from grisera.property.property_model import PropertyIn


class Sex(str, Enum):
    """
    The sexes

    Attributes:
        male (str): Male sex
        female (str): Female sex
        not_given (str): Sex was not given
    """

    male = "male"
    female = "female"
    not_given = "not given"


class ParticipantIn(BaseModel):
    """
    Model of participant to acquire from client

    Attributes:
        name (str): Name of the participant
        date_of_birth (Optional[date]): Date of birth of participant
        sex (Optional[str]): Sex of participant
        disorder (Optional[str]): Type of disorder
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant
    """

    name: Optional[str]
    date_of_birth: Optional[date]
    sex: Optional[str]
    disorder: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class BasicParticipantOut(ParticipantIn):
    """
    Basic model of participant to send to client as a result of request

    Attributes:
        id (Optional[int | str]): Id of participant returned from api
    """

    id: Optional[Union[int, str]]


class ParticipantOut(BasicParticipantOut, BaseModelOut):
    """
    Model of participant with relationships to send to client as a result of request

    Attributes:
        participant_states (Optional[List[ParticipantStateOut]]): Participant states related to this participant.
    """

    participant_states: "Optional[List[ParticipantStateOut]]"


class ParticipantsOut(BaseModelOut):
    """
    Model of participants to send to client as a result of request

    Attributes:
        participants (List[BasicParticipantOut]): Participants from database
    """

    participants: List[BasicParticipantOut] = []


# Circular import exception prevention
from grisera.participant_state.participant_state_model import ParticipantStateOut

ParticipantOut.update_forward_refs()
