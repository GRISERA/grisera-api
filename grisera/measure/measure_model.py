from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut

class Measure(tuple, Enum):
    """
    Names of measures with their datatypes

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

    familiarity = ("Familiarity", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    liking = ("Liking", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    anger = ("Anger", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    disgust = ("Disgust", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    fear = ("Fear", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    happiness = ("Happiness", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    sadness = ("Sadness", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    surprise = ("Surprise", "string", None, None, ["Absent", "Mild", "Moderate", "Intense"])
    neutral_state = ("Neutral state", "string", None, None, ["Neutral"])
    dominance = ("Dominance", "string", None, None, ["Low", "Moderate", "High"])
    arousal = ("Arousal", "string", None, None, ["Low", "Moderate", "High"])
    valence = ("Valence", "string", None, None, ["Low", "Moderate", "High"])


class MeasurePropertyIn(BaseModel):
    """
    Model of measure to acquire from client

    Attributes:
    datatype (str): Type of data
    range (Optional[str]): Range of measure
    unit (Optional[str]): Datatype property which allows for defining unit of measure
    values (Optional[List[str]]): list of available values for measure
    """

    datatype: str
    range: Optional[str]
    unit: Optional[str]
    values: Optional[List[str]]


class MeasureRelationIn(BaseModel):
    """
    Model of measure relations to acquire from client

    Attributes:
    measure_name_id (int | str): identity of the measure name
    """

    measure_name_id: Optional[Union[int, str]]


class MeasureIn(MeasurePropertyIn, MeasureRelationIn):
    """
    Full model of measure to acquire from client
    """


class BasicMeasureOut(MeasureIn):
    """
    Basic model of measure

    Attributes:
    id (Optional[Union[int, str]]): Id of measure returned from api
    """

    id: Optional[Union[int, str]]


class MeasureOut(BasicMeasureOut, BaseModelOut):
    """
    Model of measure with relations to send to client as a result of request

    Attributes:
    time_series (Optional[List[TimeSeriesOut]]): list of time series related to this measure
    measure_name (Optional[MeasureNameOut]): measure name related to this measure
    """

    time_series: "Optional[List[TimeSeriesOut]]"
    measure_name: "Optional[MeasureNameOut]"


class MeasuresOut(BaseModelOut):
    """
    Model of measures to send to client as a result of request

    Attributes:
    measures (List[BasicMeasureOut]): measures from database
    """

    measures: List[BasicMeasureOut] = []


# Circular import exception prevention
from grisera.measure_name.measure_name_model import MeasureNameOut
from grisera.time_series.time_series_model import TimeSeriesOut

MeasureOut.update_forward_refs()
