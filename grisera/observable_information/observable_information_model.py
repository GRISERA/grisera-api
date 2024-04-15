from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class ObservableInformationIn(BaseModel):
    """
    Model of information observed during experiment

    Attributes:
    modality_id (Optional[Union[int, str]]): Id od modality
    life_activity_id (Optional[Union[int, str]]): Id of life activity
    recording_id (Optional[Union[int, str]]): Id of recording
    """

    modality_id: Optional[Union[int, str]]
    life_activity_id: Optional[Union[int, str]]
    recording_id: Optional[Union[int, str]]


class BasicObservableInformationOut(ObservableInformationIn):
    """
    Model of information observed during experiment in database

    Attributes:
    id (Optional[Union[int, str]]): Id of node returned from api
    """

    id: Optional[Union[int, str]]


class ObservableInformationOut(BasicObservableInformationOut, BaseModelOut):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
    recording (Optional[RecordingOut]): recording related to this observable information
    timeSeries (Optional[List[TimeSeriesOut]]): list of time series related to this observable information
    modality (Optional[ModalityOut]): modality related to this observable information
    life_activity (Optional[LifeActivityOut]): life activity related to this observable information
    """

    recording: "Optional[RecordingOut]"
    timeSeries: "Optional[List[TimeSeriesOut]]"
    modality: "Optional[ModalityOut]"
    life_activity: "Optional[LifeActivityOut]"


class ObservableInformationsOut(BaseModelOut):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
    observable_informations (List[BasicObservableInformationOut]): Observable informations from database
    """

    observable_informations: List[BasicObservableInformationOut] = []


# Circular import exception prevention
from grisera.life_activity.life_activity_model import LifeActivityOut
from grisera.modality.modality_model import ModalityOut
from grisera.recording.recording_model import RecordingOut
from grisera.time_series.time_series_model import TimeSeriesOut

ObservableInformationOut.update_forward_refs()
