from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.measure_name.measure_name_model import MeasureNameIn
from grisera.helpers.hateoas import get_links
from grisera.measure_name.measure_name_model import (
    MeasureNameOut,
    MeasureNamesOut,
)
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class MeasureNameRouter:
    """
    Class for routing measure name based requests

    Attributes:
        measure_name_service (MeasureNameService): Service instance for measure name
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.measure_name_service = service_factory.get_measure_name_service()

    @router.post(
        "/measure_names",
        tags=["measure names"],
        response_model=MeasureNameOut,
    )
    async def create_measure_name(
        self, measure_name: MeasureNameIn, response: Response
    ):
        """
        Create measure name in database
        """
        create_response = self.measure_name_service.save_measure_name(measure_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/measure_names/{measure_name_id}",
        tags=["measure names"],
        response_model=Union[MeasureNameOut, NotFoundByIdModel],
    )
    async def get_measure_name(
        self, measure_name_id: Union[int, str], response: Response, depth: int = 0
    ):
        """
        Get measure name from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """
        get_response = self.measure_name_service.get_measure_name(
            measure_name_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/measure_names", tags=["measure names"], response_model=MeasureNamesOut
    )
    async def get_measure_names(self, response: Response):
        """
        Get measure names from database
        """

        get_response = self.measure_name_service.get_measure_names()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
