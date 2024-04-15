from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.modality.modality_model import ModalityIn
from grisera.helpers.hateoas import get_links
from grisera.modality.modality_model import ModalityOut, ModalitiesOut

from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


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
    async def create_modality(self, modality: ModalityIn, response: Response):
        """
        Create channel in database
        """
        create_response = self.modality_service.save_modality(modality)
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
        self, modality_id: Union[int, str], response: Response, depth: int = 0
    ):
        """
        Get modality from database. Depth attribute specifies how many models will be traversed to create the response.
        """
        get_response = self.modality_service.get_modality(modality_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/modalities", tags=["modalities"], response_model=ModalitiesOut)
    async def get_modalities(self, response: Response):
        """
        Get modalities from database
        """

        get_response = self.modality_service.get_modalities()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
