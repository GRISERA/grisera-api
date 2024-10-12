from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.channel.channel_model import ChannelOut, ChannelsOut, ChannelIn
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


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
    async def create_channel(self, channel: ChannelIn, response: Response, dataset_id: Union[int, str]):
        """
        Create channel in database
        """
        create_response = self.channel_service.save_channel(channel, dataset_id)
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
            self, channel_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0,
    ):

        """
        Get channel from database. Depth attribute specifies how many models will be traversed to create the response.
        """

        get_response = self.channel_service.get_channel(channel_id, dataset_id, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/channels", tags=["channels"], response_model=ChannelsOut)
    async def get_channels(self, response: Response, dataset_id: Union[int, str]):
        """
        Get channels from database
        """

        get_response = self.channel_service.get_channels(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
