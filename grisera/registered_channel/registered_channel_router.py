from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.helpers.hateoas import get_links
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.registered_channel.registered_channel_model import (
    RegisteredChannelIn,
    RegisteredChannelsOut,
    RegisteredChannelOut,
)
from grisera.services.service import service

from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class RegisteredChannelRouter:
    """
    Class for routing registered channel based requests

    Attributes:
        registered_channel (RegisteredChannelService): Service instance for registered channel
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.registered_channel_service = service_factory.get_registered_channel_service()

    @router.post(
        "/registered_channels",
        tags=["registered channels"],
        response_model=RegisteredChannelOut,
    )
    async def create_registered_channel(
        self, registered_channel: RegisteredChannelIn, response: Response
    ):
        """
        Create registered channel in database
        """
        create_response = self.registered_channel_service.save_registered_channel(
            registered_channel
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/registered_channels",
        tags=["registered channels"],
        response_model=RegisteredChannelsOut,
    )
    async def get_registered_channels(self, response: Response):
        """
        Get registered channels from database
        """

        get_response = self.registered_channel_service.get_registered_channels()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/registered_channels/{registered_channel_id}",
        tags=["registered channels"],
        response_model=Union[RegisteredChannelOut, NotFoundByIdModel],
    )
    async def get_registered_channel(
        self, registered_channel_id: Union[int, str], response: Response, depth: int = 0,
    ):
        """
        Get registered channels from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.registered_channel_service.get_registered_channel(
            registered_channel_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/registered_channels/{registered_channel_id}",
        tags=["registered channels"],
        response_model=Union[RegisteredChannelOut, NotFoundByIdModel],
    )
    async def delete_registered_channel(
        self, registered_channel_id: Union[int, str], response: Response
    ):
        """
        Delete registered channels from database
        """
        get_response = self.registered_channel_service.delete_registered_channel(
            registered_channel_id
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/registered_channels/{registered_channel_id}/relationships",
        tags=["registered channels"],
        response_model=Union[RegisteredChannelOut, NotFoundByIdModel],
    )
    async def update_registered_channel_relationships(
        self,
        registered_channel_id: Union[int, str],
        registered_channel: RegisteredChannelIn,
        response: Response,
    ):
        """
        Update registered channels relations in database
        """
        update_response = (
            self.registered_channel_service.update_registered_channel_relationships(
                registered_channel_id, registered_channel
            )
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
