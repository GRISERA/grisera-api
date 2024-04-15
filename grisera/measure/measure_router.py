from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.helpers.hateoas import get_links
from grisera.measure.measure_model import (
    MeasureIn,
    MeasuresOut,
    MeasureOut,
    MeasurePropertyIn,
    MeasureRelationIn,
)
from typing import Union
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class MeasureRouter:
    """
    Class for routing measure based requests

    Attributes:
        measure_service (MeasureService): Service instance for measures
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.measure_service = service_factory.get_measure_service()

    @router.post("/measures", tags=["measures"], response_model=MeasureOut)
    async def create_measure(self, measure: MeasureIn, response: Response):
        """
        Create measure in database
        """

        create_response = self.measure_service.save_measure(measure)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/measures", tags=["measures"], response_model=MeasuresOut)
    async def get_measures(self, response: Response):
        """
        Get measures from database
        """

        get_response = self.measure_service.get_measures()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/measures/{measure_id}",
        tags=["measures"],
        response_model=Union[MeasureOut, NotFoundByIdModel],
    )
    async def get_measure(
        self, measure_id: Union[int, str], response: Response, depth: int = 0
    ):
        """
        Get measure from database. Depth attribute specifies how many models will be traversed to create the response.
        """

        get_response = self.measure_service.get_measure(measure_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/measures/{measure_id}",
        tags=["measures"],
        response_model=Union[MeasureOut, NotFoundByIdModel],
    )
    async def delete_measure(self, measure_id: Union[int, str], response: Response):
        """
        Delete measure from database
        """
        get_response = self.measure_service.delete_measure(measure_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/measures/{measure_id}",
        tags=["measures"],
        response_model=Union[MeasureOut, NotFoundByIdModel],
    )
    async def update_measure(
        self,
        measure_id: Union[int, str],
        measure: MeasurePropertyIn,
        response: Response,
    ):
        """
        Update measure model in database
        """
        update_response = self.measure_service.update_measure(measure_id, measure)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/measures/{measure_id}/relationships",
        tags=["measures"],
        response_model=Union[MeasureOut, NotFoundByIdModel],
    )
    async def update_measure_relationships(
        self,
        measure_id: Union[int, str],
        measure: MeasureRelationIn,
        response: Response,
    ):
        """
        Update measure relations in database
        """
        update_response = self.measure_service.update_measure_relationships(
            measure_id, measure
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
