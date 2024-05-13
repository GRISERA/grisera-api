from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class FacialHair(str, Enum):
    heavy = "Heavy"
    some = "Some"
    no = "None"


class AppearanceOcclusionIn(BaseModel):
    """
    Model of appearance occlusion to acquire from client

    Attributes:
        glasses (bool): Does appearance contain glasses
        beard (FacialHair): Length of beard
        moustache (FacialHair): Length of moustache
    """

    beard: FacialHair
    moustache: FacialHair
    glasses: bool


class BasicAppearanceOcclusionOut(AppearanceOcclusionIn):
    """
    Basic model of appearance occlusion to send to client as a result of request

    Attributes:
        id (Optional[Union[int, str]]): Id of appearance occlusion model returned from api
    """

    id: Optional[Union[int, str]]


class AppearanceOcclusionOut(BasicAppearanceOcclusionOut, BaseModelOut):
    """
    Model of appearance occlusion with relationships to send to client as a result of request

    Attributes:
        participant_states (Optional[List[ParticipantStateOut]]): List of participant states related to this
            personality
    """

    participant_states: "Optional[List[ParticipantStateOut]]"


class AppearanceSomatotypeIn(BaseModel):
    """
    Model of appearance somatotype to acquire from client

    Attributes:
        ectomorph (float): Range of ectomorph appearance measure
        endomorph (float): Range of endomorph appearance measure
        mesomorph (float): Range of mesomorph appearance measure

    """

    ectomorph: float
    endomorph: float
    mesomorph: float


class BasicAppearanceSomatotypeOut(AppearanceSomatotypeIn):
    """
    Basic model of appearance somatotype to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of appearance somatotype model returned from api

    """

    id: Optional[Union[int, str]]


class AppearanceSomatotypeOut(BasicAppearanceSomatotypeOut, BaseModelOut):
    """
    Model of appearance somatotype with relationships to send to client as a result of request

    Attributes:
        participant_states (Optional[List[ParticipantStateOut]]): List of participant states related to this
            personality
    """

    participant_states: "Optional[List[ParticipantStateOut]]"


class AppearancesOut(BaseModelOut):
    """
    Model of appearances to send to client as a result of request

    Attributes:
        appearances (List[Union[BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut]]): Appearances from database
    """

    appearances: List[
        Union[BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut]
    ] = []


# Circular import exception prevention
from grisera.participant_state.participant_state_model import ParticipantStateOut

AppearanceOcclusionOut.update_forward_refs()
AppearanceSomatotypeOut.update_forward_refs()
