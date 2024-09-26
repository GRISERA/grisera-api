from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class MeasureName(tuple, Enum):
    """
    Names of measures with their types

    Attributes:
    familiarity (tuple): Familiarity
    liking (tuple): Liking
    anger (tuple): Anger
    disgust (tuple): Disgust
    fear (tuple): Fear
    happiness (tuple): Happiness
    sadness (tuple): Sadness
    surprise (tuple): Surprise
    neutral_state (tuple): Neutral state
    dominance (tuple): Dominance
    arousal (tuple): Arousal
    valence (tuple): Valence
    """

    familiarity = ("Familiarity", "User defined")
    liking = ("Liking", "Ekman")
    anger = ("Anger", "Ekman")
    disgust = ("Disgust", "Ekman")
    fear = ("Fear", "Ekman")
    happiness = ("Happiness", "Ekman")
    sadness = ("Sadness", "Ekman")
    surprise = ("Surprise", "Ekman")
    neutral_state = ("Neutral state", "Neutral")
    dominance = ("Dominance", "PAD")
    arousal = ("Arousal", "PAD")
    valence = ("Valence", "PAD")


class MeasureNameIn(BaseModel):
    """
    Model of measure name

    Attributes:
    name (str): Name of measure
    type (str): Type of the measure name
    """

    name: str
    type: str


class BasicMeasureNameOut(MeasureNameIn):
    """
    Model of measure name in dataset

    Attributes:
    id (Optional[Union[int, str]]): Id of measure name returned from api
    """

    id: Optional[Union[int, str]]


class MeasureNameOut(BasicMeasureNameOut, BaseModelOut):
    """
    Model of measure name to send to client as a result of request

    Attributes:
    measures (List[MeasureOut]): list of measures related to this measure name
    """

    measures: "Optional[List[MeasureOut]]"


class MeasureNamesOut(BaseModelOut):
    """
    Model of measure names to send to client as a result of request

    Attributes:
    measure_names (List[BasicMeasureNameOut]): Measure names from database
    """

    measure_names: List[BasicMeasureNameOut] = []


# Circular import exception prevention
from grisera.measure.measure_model import MeasureOut

MeasureNameOut.update_forward_refs()
