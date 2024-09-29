from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.registered_data.registered_data_model import (
    RegisteredDataIn,
    RegisteredDataOut,
    RegisteredDataNodesOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class RegisteredDataRouter:
    """
    Class for routing registered data based requests

    Attributes:
        registered_data_service (RegisteredDataService): Service instance for registered data
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.registered_data_service = service_factory.get_registered_data_service()

    @router.post(
        "/registered_data", tags=["registered data"], response_model=RegisteredDataOut
    )
    async def create_registered_data(
            self, registered_data: RegisteredDataIn, response: Response, dataset_id: Union[int, str]
    ):
        """
        Create registered data in database
        """
        create_response = self.registered_data_service.save_registered_data(
            registered_data, dataset_id
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def get_registered_data(
            self, registered_data_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get registered data from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.registered_data_service.get_registered_data(
            registered_data_id, dataset_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/registered_data",
        tags=["registered data"],
        response_model=RegisteredDataNodesOut,
    )
    async def get_registered_data_nodes(self, response: Response, dataset_id: Union[int, str]):
        """
        Get registered data from database
        """

        get_response = self.registered_data_service.get_registered_data_nodes(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def delete_registered_data(
            self, registered_data_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete registered data from database
        """
        get_response = self.registered_data_service.delete_registered_data(
            registered_data_id, dataset_id
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def update_registered_data(
            self,
            registered_data_id: Union[int, str],
            registered_data: RegisteredDataIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update registered data model in database
        """
        update_response = self.registered_data_service.update_registered_data(
            registered_data_id, registered_data, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
