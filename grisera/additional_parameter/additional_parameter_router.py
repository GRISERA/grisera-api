from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.additional_parameter.additional_parameter_model import (
    AdditionalParameterIn,
    AdditionalParameterOut,
    AdditionalParametersOut,
)
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class AdditionalParameterRouter:
    """
    Class for routing additional parameter based requests

    Attributes:
        additional_parameter_service (AdditionalParameterService): Service instance for additional parameters
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.additional_parameter_service = service_factory.get_additional_parameter_service()

    @router.post("/parameters", tags=["parameters"], response_model=AdditionalParameterOut)
    async def create_parameter(self, parameter: AdditionalParameterIn, response: Response, dataset_id: Union[int, str]):
        """
        Create additional parameter in database
        """

        create_response = self.additional_parameter_service.save_additional_parameter(parameter, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/parameters", tags=["parameters"], response_model=AdditionalParametersOut)
    async def get_parameters(self, response: Response, dataset_id: Union[int, str]):
        """
        Get additional parameters from database
        """

        get_response = self.additional_parameter_service.get_additional_parameters(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/parameters/{parameter_id}",
        tags=["parameters"],
        response_model=Union[AdditionalParameterOut, NotFoundByIdModel],
    )
    async def get_parameter(
            self, parameter_id: Union[str, int], response: Response, dataset_id: Union[int, str]
    ):
        """
        Get additional parameter from database
        """

        get_response = self.additional_parameter_service.get_additional_parameter(parameter_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/parameters/{parameter_id}",
        tags=["parameters"],
        response_model=Union[AdditionalParameterOut, NotFoundByIdModel],
    )
    async def delete_parameter(
            self, parameter_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete additional parameter from database
        """
        delete_response = self.additional_parameter_service.delete_additional_parameter(parameter_id, dataset_id)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response

    @router.put(
        "/parameters/{parameter_id}",
        tags=["parameters"],
        response_model=Union[AdditionalParameterOut, NotFoundByIdModel],
    )
    async def update_parameter(
            self,
            parameter_id: Union[int, str],
            parameter: AdditionalParameterIn,
            response: Response,
            dataset_id: Union[int, str]
    ):
        """
        Update additional parameter model in database
        """
        update_response = self.additional_parameter_service.update_additional_parameter(
            parameter_id, parameter, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response