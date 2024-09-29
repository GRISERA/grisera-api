from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.activity_execution.activity_execution_model import (
    ActivityExecutionIn,
    ActivityExecutionOut,
    ActivityExecutionsOut,
    ActivityExecutionPropertyIn,
    ActivityExecutionRelationIn,
)
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ActivityExecutionRouter:
    """
    Class for routing activity execution based requests

    Attributes:
        activity_execution_service (ActivityExecutionService): Service instance for activity execution
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.activity_execution_service = service_factory.get_activity_execution_service()

    @router.post(
        "/activity_executions",
        tags=["activity executions"],
        response_model=ActivityExecutionOut,
    )
    async def create_activity_execution(
            self, activity_execution: ActivityExecutionIn, response: Response, dataset_id: Union[int, str]
    ):
        """
        Create activity execution in database
        """
        create_response = self.activity_execution_service.save_activity_execution(
            activity_execution, dataset_id
        )

        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/activity_executions",
        tags=["activity executions"],
        response_model=ActivityExecutionsOut,
    )
    async def get_activity_executions(self, response: Response, dataset_id: Union[int, str]):

        """
        Get activity executions from database
        """

        get_response = self.activity_execution_service.get_activity_executions(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/activity_executions/{activity_execution_id}",
        tags=["activity executions"],
        response_model=Union[ActivityExecutionOut, NotFoundByIdModel],
    )
    async def get_activity_execution(
            self, activity_execution_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0,
    ):

        """
        Get activity execution from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.activity_execution_service.get_activity_execution(
            activity_execution_id, dataset_id, depth
        )

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/activity_executions/{activity_execution_id}",
        tags=["activity executions"],
        response_model=Union[ActivityExecutionOut, NotFoundByIdModel],
    )
    async def delete_activity_execution(
            self, activity_execution_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete activity executions from database
        """
        get_response = self.activity_execution_service.delete_activity_execution(
            activity_execution_id, dataset_id
        )

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/activity_executions/{activity_execution_id}",
        tags=["activity executions"],
        response_model=Union[ActivityExecutionOut, NotFoundByIdModel],
    )
    async def update_activity_execution(
            self,
            activity_execution_id: Union[int, str],
            activity_execution: ActivityExecutionPropertyIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update activity execution model in database
        """
        update_response = self.activity_execution_service.update_activity_execution(
            activity_execution_id, activity_execution, dataset_id
        )

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/activity_executions/{activity_execution_id}/relationships",
        tags=["activity executions"],
        response_model=Union[ActivityExecutionOut, NotFoundByIdModel],
    )
    async def update_activity_execution_relationships(
            self,
            activity_execution_id: Union[int, str],
            activity_execution: ActivityExecutionRelationIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update activity executions relations in database
        """
        update_response = (
            self.activity_execution_service.update_activity_execution_relationships(
                activity_execution_id, activity_execution, dataset_id
            )
        )

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
