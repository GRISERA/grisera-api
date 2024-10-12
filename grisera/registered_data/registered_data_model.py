from typing import List, Union, Optional

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut
from grisera.property.property_model import PropertyIn


class RegisteredDataIn(BaseModel):
    """
    Model of registered data to acquire from client

    Attributes:
    source (str): URI address where recorded data is located

    """

    source: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class BasicRegisteredDataOut(RegisteredDataIn):
    """
    Basic model of registered data to send to client as a result of request

    Attributes:
    id (Optional[Union[int, str]]): Id of registered data returned from api
    """

    id: Optional[Union[int, str]]


class RegisteredDataOut(BasicRegisteredDataOut, BaseModelOut):
    """
    Model of registered data with relationships to send to client as a result of request

    Attributes:
    registered_channels (Optional[List[RegisteredChannelOut]]): registered channels related to this registered data
    """

    registered_channels: "Optional[List[RegisteredChannelOut]]"


class RegisteredDataNodesOut(BaseModelOut):
    """
    Model of registered data nodes to send to client as a result of request

    Attributes:
    registered_data_nodes (List[BasicRegisteredDataOut]): Registered Data nodes from database
    """

    registered_data_nodes: List[BasicRegisteredDataOut] = []


# Circular import exception prevention
from grisera.registered_channel.registered_channel_model import RegisteredChannelOut

RegisteredDataOut.update_forward_refs()
