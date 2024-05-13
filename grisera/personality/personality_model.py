from typing import Optional, List, Union

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class PersonalityBigFiveIn(BaseModel):
    """
    Model of personality big five model to acquire from client

    Attributes:
        agreeableness (float): Scale of being kind, sympathetic, cooperative, warm, and considerate
        conscientiousness (float): Scale of being neat, and systematic
        extroversion (float): Scale of being outgoing, talkative, energetic
        neuroticism (float): Scale of lack of self-control, poor ability to manage psychological stress
        openess (float): Scale of openness (Intellect) reflects imagination, creativity

    """

    agreeableness: float
    conscientiousness: float
    extroversion: float
    neuroticism: float
    openess: float


class BasicPersonalityBigFiveOut(PersonalityBigFiveIn):
    """
    Basic model of personality big five model to send to client as a result of request

    Attributes:
        id (Optional[int | str]): Id of personality big five model returned from api
    """

    id: Optional[Union[int, str]]


class PersonalityBigFiveOut(BasicPersonalityBigFiveOut, BaseModelOut):
    """
    Model of personality big five model with relationships to send to client as a result of request

    Attributes:
        participant_states (Optional[List[ParticipantStateOut]]): List of participant states related to this
            personality
    """

    participant_states: "Optional[List[ParticipantStateOut]]"


class PersonalityPanasIn(BaseModel):
    """
    Model of personality panas to acquire from client

    Attributes:
        negative_affect (float): Scale of negative affect to community
        positive_affect (float): Scale of positive affect to community
    """

    negative_affect: float
    positive_affect: float


class BasicPersonalityPanasOut(PersonalityPanasIn):
    """
    Basic model of personality panas to send to client as a result of request

    Attributes:
        id (Optional[int | str]): Id of personality panas returned from api
    """

    id: Optional[Union[int, str]]


class PersonalityPanasOut(BasicPersonalityPanasOut, BaseModelOut):
    """
    Model of personality panas with relationships to send to client as a result of request

    Attributes:
        participant_states (Optional[List[ParticipantStateOut]]): List of participant states related to this
            personality
    """

    participant_states: "Optional[List[ParticipantStateOut]]"


class PersonalitiesOut(BaseModelOut):
    """
    Model of personalities to send to client as a result of request

    Attributes:
        personalities (List[Union[BasicPersonalityBigFiveOut, BasicPersonalityPanasOut]]): Personalities from database
    """

    personalities: List[
        Union[BasicPersonalityBigFiveOut, BasicPersonalityPanasOut]
    ] = []


# Circular import exception prevention
from grisera.participant_state.participant_state_model import ParticipantStateOut

PersonalityBigFiveOut.update_forward_refs()
PersonalityPanasOut.update_forward_refs()
