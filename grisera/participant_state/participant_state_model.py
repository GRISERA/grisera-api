from typing import List
from typing import Optional, Union

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut
from grisera.property.property_model import PropertyIn


class ParticipantStatePropertyIn(BaseModel):
    """
    Model of participant state to acquire from client

    Attributes:
        age (Optional[int]): Age of participant state
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant state
    """

    age: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class ParticipantStateRelationIn(BaseModel):
    """
    Model of participant state relations to acquire from client

    Attributes:
        participant_id (Optional[int | str]): Participant whose state is described
        personality_ids List(Optional[int | str]): identities of personalities describing participant
        appearance_ids List(Optional[int | str]): identities of appearances describing participant
    """

    participant_id: Optional[Union[int, str]] = None
    personality_ids: List[Optional[Union[int, str]]] = None
    appearance_ids: List[Optional[Union[int, str]]] = None


class ParticipantStateIn(ParticipantStatePropertyIn, ParticipantStateRelationIn):
    """
    Full model of participant state to acquire from client
    """


class BasicParticipantStateOut(ParticipantStateIn):
    """
    Basic model of participant

    Attributes:
        id (Optional[int | str]): Id of participant returned from api
    """

    id: Optional[Union[int, str]]


class ParticipantStateOut(BasicParticipantStateOut, BaseModelOut):
    """
    Model of participant state with optional related fields to send to client as a result of request

    Attributes:
        participations (Optional[List[ParticipationOut]]): participations with this participant state
        participant (Optional[ParticipantOut]): participant related to this participant state
        appearances (Optional[Union[AppearanceSomatotypeOut, AppearanceOcclusionOut]]): appearances related to
            this participant state
        personalities (Optional[Union[PersonalityBigFiveOut, PersonalityPanasOut]]): personalities related to this
            participant state
    """

    participations: "Optional[List[ParticipationOut]]"
    participant: "Optional[ParticipantOut]"
    appearances: "Optional[List[Union[AppearanceSomatotypeOut, AppearanceOcclusionOut]]]"
    personalities: "Optional[List[Union[PersonalityBigFiveOut, PersonalityPanasOut]]]"


class ParticipantStatesOut(BaseModelOut):
    """
    Model of participant states to send to client as a result of request

    Attributes:
        participant_states (List[BasicParticipantStateOut]): Participant states from database
    """

    participant_states: List[BasicParticipantStateOut] = []


# Circular import exception prevention
from grisera.participation.participation_model import ParticipationOut
from grisera.participant.participant_model import ParticipantOut
from grisera.personality.personality_model import PersonalityBigFiveOut, PersonalityPanasOut
from grisera.appearance.appearance_model import AppearanceSomatotypeOut, AppearanceOcclusionOut

ParticipantStateOut.update_forward_refs()
