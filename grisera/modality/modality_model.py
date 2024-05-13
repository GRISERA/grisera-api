from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class Modality(str, Enum):
    """
    Type of observable information

    Attributes:
    facial_expressions (str): Facial expressions
    body_posture (str): Body posture
    eye_gaze (str): Eye gaze
    head_movement (str): Head movement
    gestures (str): Gestures
    motion (str): Motion
    prosody_of_speech (str): Prosody of speech
    vocalization (str): Vocalization
    heart_rate (str): Heart rate
    hrv (str): HRV
    muscle_tension (str): Muscle tension
    skin_conductance (str): Skin conductance
    resp_intensity_and_period (str): RESP intensity and period
    peripheral_temperature (str): Peripheral temperature
    neural_activity (str): Neural activity
    """

    facial_expressions = "facial expressions"
    body_posture = "body posture"
    eye_gaze = "eye gaze"
    head_movement = "head movement"
    gestures = "gestures"
    motion = "motion"
    prosody_of_speech = "prosody of speech"
    vocalization = "vocalization"
    heart_rate = "heart rate"
    hrv = "HRV"
    muscle_tension = "muscle tension"
    skin_conductance = "skin conductance"
    resp_intensity_and_period = "RESP intensity"
    peripheral_temperature = "peripheral temperature"
    neural_activity = "neural activity"


class ModalityIn(BaseModel):
    """
    Model of modality observed during experiment

    Attributes:
    modality (str): Type of observable information
    """

    modality: str


class BasicModalityOut(ModalityIn):
    """
    Model of modality in database

    Attributes:
    id (Optional[Union[int, str]]): Id of modality returned from api
    """

    id: Optional[Union[int, str]]


class ModalityOut(BasicModalityOut, BaseModelOut):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
    observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
        this modality
    """

    observable_informations: "Optional[List[ObservableInformationOut]]"


class ModalitiesOut(BaseModelOut):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
    modalities (List[BasicModalityOut]): Modalities from database
    """

    modalities: List[BasicModalityOut] = []


# Circular import exception prevention
from grisera.observable_information.observable_information_model import ObservableInformationOut

ModalityOut.update_forward_refs()
