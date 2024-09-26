from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class Types(tuple, Enum):
    """
    Types of channel

    Attributes:
    audio: Audio channel
    bvp: BVP channel
    chest_size: Chest size channel
    depth_video: Depth video channel
    ecg: Electrocardiography channel
    eda: Electrodermal activity channel
    eeg: Electroencephalography channel
    emg: Electromyography channel
    rgb_video: RGB video channel
    temperature: Temperature channel
    """

    audio = ("Audio", "Audio channel")
    bvp = ("BVP", "Blood Volume Pulse (BVP) channel")
    chest_size = ("Chest size", "Chest size channel")
    depth_video = ("Depth video", "Depth video channel")
    ecg = ("ECG", "Electrocardiography channel")
    eda = ("EDA", "Electrodermal activity channel")
    eeg = ("EEG", "Electroencephalography channel")
    emg = ("EMG", "Electromyography channel")
    rgb_video = ("RGB video", "RGB video channel")
    temperature = ("Temperature", "Temperature channel")


class ChannelIn(BaseModel):
    """
    Model of channel

    Attributes:
    type (str): Type of the channel
    """

    type: str
    description: str


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
