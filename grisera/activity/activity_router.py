from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.activity.activity_model import ActivityIn
from grisera.activity.activity_model import ActivityOut, ActivitiesOut
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ActivityRouter:
    """
    Class for routing activity based requests

    Attributes:
        activity_service (ActivityService): Service instance for activity
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.activity_service = service_factory.get_activity_service()

    @router.post("/activities", tags=["activities"], response_model=ActivityOut)
    async def create_activity(self, activity: ActivityIn, response: Response, dataset_id: Union[int, str]):
        """
        Create activity in dataset
        """
        create_response = self.activity_service.save_activity(activity, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/activities/{activity_id}", tags=["activities"],
                response_model=Union[ActivityOut, NotFoundByIdModel], )
    async def get_activity(self, activity_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0):
        """
        Get activity from database. Depth attribute specifies how many models will be traversed to create the response.
        """
        get_response = self.activity_service.get_activity(activity_id, dataset_id, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/activities", tags=["activities"], response_model=ActivitiesOut)
    async def get_activities(self, response: Response, dataset_id: Union[int, str]):
        """
        Get activities from dataset
        """

        get_response = self.activity_service.get_activities(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/activities/{activity_id}", tags=["activities"],
                   response_model=Union[ActivityOut, NotFoundByIdModel])
    async def delete_activity(self, activity_id: Union[int, str], response: Response, dataset_id: Union[int, str]):
        """
        Delete activity from dataset
        """
        get_response = self.activity_service.delete_activity(activity_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/activities/{activity_id}", tags=["activities"],
                response_model=Union[ActivityOut, NotFoundByIdModel])
    async def update_activity(self, activity_id: Union[int, str], activity: ActivityIn, response: Response,
                              dataset_id: Union[int, str]):
        """
        Update activity model in dataset
        """
        update_response = self.activity_service.update_activity(activity_id, activity, dataset_id)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
