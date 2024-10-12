from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.modality.modality_model import ModalityIn
from grisera.modality.modality_model import ModalityOut, ModalitiesOut
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ModalityRouter:
    """
    Class for routing modality based requests

    Attributes:
        modality_service (ModalityService): Service instance for modality
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.modality_service = service_factory.get_modality_service()

    @router.post(
        "/modalities",
        tags=["modalities"],
        response_model=ModalityOut,
    )
    async def create_modality(self, modality: ModalityIn, response: Response, dataset_id: Union[int, str]):
        """
        Create channel in database
        """
        create_response = self.modality_service.save_modality(modality, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/modalities/{modality_id}",
        tags=["modalities"],
        response_model=Union[ModalityOut, NotFoundByIdModel],
    )
    async def get_modality(
            self, modality_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):

        """
        Get modality from database. Depth attribute specifies how many models will be traversed to create the response.
        """

        get_response = self.modality_service.get_modality(modality_id, dataset_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/modalities", tags=["modalities"], response_model=ModalitiesOut)
    async def get_modalities(self, response: Response, dataset_id: Union[int, str]):
        """
        Get modalities from database
        """

        get_response = self.modality_service.get_modalities(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
