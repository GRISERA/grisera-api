from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class Type(str, Enum):
    """
    Types of channel

    Attributes:
    audio (str): Audio channel
    bvp (str): BVP channel
    chest_size (str): Chest size channel
    depth_video (str): Depth video channel
    ecg (str): ECG channel
    eda (str): EDA channel
    eeg (str): EEG channel
    emg (str): EMG channel
    rgb_video (str): RGB video channel
    temperature (str): Temperature channel
    """

    audio = "Audio"
    bvp = "BVP"
    chest_size = "Chest size"
    depth_video = "Depth video"
    ecg = "ECG"
    eda = "EDA"
    eeg = "EEG"
    emg = "EMG"
    rgb_video = "RGB video"
    temperature = "Temperature"


class ChannelIn(BaseModel):
    """
    Model of channel

    Attributes:
    type (str): Type of the channel
    """

    type: str


class BasicChannelOut(ChannelIn):
    """
    Model of channel in database

    Attributes:
    id (Optional[Union[int, str]]): Id of channel returned from api
    """

    id: Optional[Union[int, str]]


class ChannelOut(BasicChannelOut, BaseModelOut):
    """
    Model of channel to send to client as a result of request

    Attributes:
    registered_channels (Optional[List[RegisteredChannelOut]]): registered channels related to this channel

    """

    registered_channels: "Optional[List[RegisteredChannelOut]]"


class ChannelsOut(BaseModelOut):
    """
    Model of channels to send to client as a result of request

    Attributes:
    channels (List[BasicChannelOut]): Channels from database
    """

    channels: List[BasicChannelOut] = []


# Circular import exception prevention
from grisera.registered_channel.registered_channel_model import RegisteredChannelOut

ChannelOut.update_forward_refs()
