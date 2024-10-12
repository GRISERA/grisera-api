from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.life_activity.life_activity_model import LifeActivityIn
from grisera.life_activity.life_activity_model import (
    LifeActivityOut,
    LifeActivitiesOut,
)
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class LifeActivityRouter:
    """
    Class for routing life activity based requests

    Attributes:
        life_activity_service (LifeActivityService): Service instance for life activity
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.life_activity_service = service_factory.get_life_activity_service()

    @router.post(
        "/life_activities",
        tags=["life activities"],
        response_model=LifeActivityOut,
    )
    async def create_life_activity(
            self, life_activity: LifeActivityIn, response: Response, dataset_id: Union[int, str]
    ):
        """
        Create channel in database
        """
        create_response = self.life_activity_service.save_life_activity(life_activity, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/life_activities/{life_activity_id}",
        tags=["life activities"],
        response_model=Union[LifeActivityOut, NotFoundByIdModel],
    )
    async def get_life_activity(
            self, life_activity_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):

        """
        Get life activity from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.life_activity_service.get_life_activity(
            life_activity_id, dataset_id, depth
        )

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/life_activities", tags=["life activities"], response_model=LifeActivitiesOut
    )
    async def get_life_activities(self, response: Response, dataset_id: Union[int, str]):

        """
        Get life activities from database
        """

        get_response = self.life_activity_service.get_life_activities(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
