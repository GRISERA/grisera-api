from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.appearance.appearance_model import (
    AppearanceOcclusionIn,
    AppearanceOcclusionOut,
    AppearanceSomatotypeIn,
    AppearanceSomatotypeOut,
    AppearancesOut,
)
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class AppearanceRouter:
    """
    Class for routing appearance based requests

    Attributes:
        appearance_service (AppearanceService): Service instance for appearance
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.appearance_service = service_factory.get_appearance_service()

    @router.post(
        "/appearance/occlusion_model",
        tags=["appearance"],
        response_model=AppearanceOcclusionOut,
    )
    async def create_appearance_occlusion(
            self, appearance: AppearanceOcclusionIn, response: Response, dataset_id: Union[int, str]
    ):

        """
        Create appearance occlusion model in database
        """

        create_response = self.appearance_service.save_appearance_occlusion(appearance, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post(
        "/appearance/somatotype_model",
        tags=["appearance"],
        response_model=AppearanceSomatotypeOut,
    )
    async def create_appearance_somatotype(
            self, appearance: AppearanceSomatotypeIn, response: Response, dataset_id: Union[int, str]
    ):

        """
        Create appearance somatotype model in database
        """

        create_response = self.appearance_service.save_appearance_somatotype(appearance, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/appearance", tags=["appearance"], response_model=AppearancesOut)
    async def get_appearances(self, response: Response, dataset_id: Union[int, str]):
        """
        Get appearances from database
        """

        get_response = self.appearance_service.get_appearances(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/appearance/{appearance_id}",
        tags=["appearance"],
        response_model=Union[
            AppearanceSomatotypeOut, AppearanceOcclusionOut, NotFoundByIdModel
        ],
    )
    async def get_appearance(
            self, appearance_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):

        """
        Get appearance from database. Depth attribute specifies how many models will be traversed to create the response
        """

        get_response = self.appearance_service.get_appearance(appearance_id, dataset_id, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/appearance/{appearance_id}",
        tags=["appearance"],
        response_model=Union[
            AppearanceSomatotypeOut, AppearanceOcclusionOut, NotFoundByIdModel
        ],
    )
    async def delete_appearance(
            self, appearance_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):

        """
        Delete appearance from database
        """
        get_response = self.appearance_service.delete_appearance(appearance_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/appearance/occlusion_model/{appearance_id}",
        tags=["appearance"],
        response_model=Union[AppearanceOcclusionOut, NotFoundByIdModel],
    )
    async def update_appearance_occlusion(
            self,
            appearance_id: Union[int, str],
            appearance: AppearanceOcclusionIn,
            response: Response,
            dataset_id: Union[int, str]
    ):
        """
        Update appearance occlusion model in database
        """
        update_response = self.appearance_service.update_appearance_occlusion(
            appearance_id, appearance, dataset_id
        )

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/appearance/somatotype_model/{appearance_id}",
        tags=["appearance"],
        response_model=Union[AppearanceSomatotypeOut, NotFoundByIdModel],
    )
    async def update_appearance_somatotype(
            self,
            appearance_id: Union[int, str],
            appearance: AppearanceSomatotypeIn,
            response: Response,
            dataset_id: Union[int, str]
    ):
        """
        Update appearance somatotype model in database
        """
        update_response = self.appearance_service.update_appearance_somatotype(
            appearance_id, appearance, dataset_id
        )

        if update_response.errors is not None:
            response.status_code = (
                404 if type(update_response) == NotFoundByIdModel else 422
            )

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
