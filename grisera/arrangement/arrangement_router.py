from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.arrangement.arrangement_model import (
    ArrangementOut,
    ArrangementsOut,
    ArrangementIn,
)
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


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
            self, arrangement_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get arrangement from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """
        get_response = self.arrangement_service.get_arrangement(arrangement_id, dataset_id, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/arrangements", tags=["arrangements"], response_model=ArrangementsOut)
    async def get_arrangements(self, response: Response, dataset_id: Union[int, str]):
        """
        Get arrangements from dataset
        """

        get_response = self.arrangement_service.get_arrangements(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.post("/arrangements", tags=["arrangements"], response_model=ArrangementOut)
    async def create_activity(self, arrangement: ArrangementIn, response: Response, dataset_id: Union[int, str]):
        """
        Create arrangement in dataset
        """
        create_response = self.arrangement_service.save_arrangement(arrangement, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/arrangements/{arrangement_id}", tags=["arrangements"],
                   response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def delete_arrangement(self, arrangement_id: Union[int, str], response: Response, dataset_id: Union[int, str]):
        """
        Delete arrangement from dataset
        """
        get_response = self.arrangement_service.delete_arrangement(arrangement_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/arrangements/{arrangement_id}", tags=["arrangements"],
                response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def update_arrangement(self, arrangement_id: Union[int, str], arrangement: ArrangementIn, response: Response,
                                 dataset_id: Union[int, str]):
        """
        Update arrangement model in dataset
        """
        update_response = self.arrangement_service.update_arrangement(arrangement_id, arrangement, dataset_id)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
