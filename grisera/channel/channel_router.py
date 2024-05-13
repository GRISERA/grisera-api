from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.helpers.hateoas import get_links
from grisera.channel.channel_model import ChannelOut, ChannelsOut, ChannelIn
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class ChannelRouter:
    """
    Class for routing channel based requests

    Attributes:
        channel_service (ChannelService): Service instance for channel
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.channel_service = service_factory.get_channel_service()

    @router.post(
        "/channels",
        tags=["channels"],
        response_model=ChannelOut,
    )
    async def create_channel(self, channel: ChannelIn, response: Response, dataset_name: str):
        """
        Create channel in database
        """
        create_response = self.channel_service.save_channel(channel, dataset_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/channels/{channel_id}",
        tags=["channels"],
        response_model=Union[ChannelOut, NotFoundByIdModel],
    )
    async def get_channel(
        self, channel_id: Union[int, str], response: Response, dataset_name: str, depth: int = 0,
    ):

        """
        Get channel from database. Depth attribute specifies how many models will be traversed to create the response.
        """

        get_response = self.channel_service.get_channel(channel_id,dataset_name, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/channels", tags=["channels"], response_model=ChannelsOut)
    async def get_channels(self, response: Response, dataset_name: str):
        """
        Get channels from database
        """

        get_response = self.channel_service.get_channels(dataset_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
