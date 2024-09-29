from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.measure_name.measure_name_model import MeasureNameIn
from grisera.measure_name.measure_name_model import (
    MeasureNameOut,
    MeasureNamesOut,
)
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class MeasureNameRouter:
    """
    Class for routing measure name based requests

    Attributes:
        measure_name_service (MeasureNameService): Service instance for measure name
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.measure_name_service = service_factory.get_measure_name_service()

    @router.get(
        "/measure_names/{measure_name_id}",
        tags=["measure names"],
        response_model=Union[MeasureNameOut, NotFoundByIdModel],
    )
    async def get_measure_name(
            self, measure_name_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get measure name from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.measure_name_service.get_measure_name(
            measure_name_id, dataset_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/measure_names", tags=["measure names"], response_model=MeasureNamesOut
    )
    async def get_measure_names(self, response: Response, dataset_id: Union[int, str]):
        """
        Get measure names from dataset
        """

        get_response = self.measure_name_service.get_measure_names(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.post("/measure_names", tags=["measure names"], response_model=MeasureNameOut)
    async def create_measure_name(self, measure_name: MeasureNameIn, response: Response, dataset_id: Union[int, str]):
        """
        Create measure_name in dataset
        """
        create_response = self.measure_name_service.save_measure_name(measure_name, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/measure_names/{measure_name_id}", tags=["measure names"],
                   response_model=Union[MeasureNameOut, NotFoundByIdModel])
    async def delete_measure_name(self, measure_name_id: Union[int, str], response: Response, dataset_id: Union[int, str]):
        """
        Delete measure_name from dataset
        """
        get_response = self.measure_name_service.delete_measure_name(measure_name_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/measure_names/{measure_name_id}", tags=["measure names"],
                response_model=Union[MeasureNameOut, NotFoundByIdModel])
    async def update_measure_name(self, measure_name_id: Union[int, str], measure_name: MeasureNameIn,
                                  response: Response,
                                  dataset_id: Union[int, str]):
        """
        Update measure_name model in dataset
        """
        update_response = self.measure_name_service.update_measure_name(measure_name_id, measure_name, dataset_id)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
