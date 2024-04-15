from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.helpers.hateoas import get_links
from grisera.arrangement.arrangement_model import (
    ArrangementOut,
    ArrangementsOut,
)
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class ArrangementRouter:
    """
    Class for routing arrangement based requests

    Attributes:
        arrangement_service (ArrangementService): Service instance for arrangement
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.arrangement_service = service_factory.get_arrangement_service()

    @router.get(
        "/arrangements/{arrangement_id}",
        tags=["arrangements"],
        response_model=Union[ArrangementOut, NotFoundByIdModel],
    )
    async def get_arrangement(
        self, arrangement_id: Union[int, str], response: Response, depth: int = 0
    ):
        """
        Get arrangement from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """
        get_response = self.arrangement_service.get_arrangement(arrangement_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/arrangements", tags=["arrangements"], response_model=ArrangementsOut)
    async def get_arrangements(self, response: Response):
        """
        Get arrangements from database
        """

        get_response = self.arrangement_service.get_arrangements()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
