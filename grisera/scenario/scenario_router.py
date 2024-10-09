from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.activity_execution.activity_execution_model import (
    ActivityExecutionOut,
    ActivityExecutionIn,
)
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.scenario.scenario_model import (
    ScenarioIn,
    ScenarioOut,
    OrderChangeIn,
    OrderChangeOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ScenarioRouter:
    """
    Class for routing scenario based requests

    Attributes:
        scenario_service (ScenarioService): Service instance for scenarios
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.scenario_service = service_factory.get_scenario_service()

    @router.post("/scenarios", tags=["scenarios"], response_model=ScenarioOut)
    async def create_scenario(self, scenario: ScenarioIn, response: Response, dataset_id: Union[int, str]):
        """
        Create scenario in database
        """
        create_response = self.scenario_service.save_scenario(scenario, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/scenarios/{scenario_id}", tags=["scenarios"], response_model=Union[ScenarioOut, NotFoundByIdModel])
    async def create_scenario_execution(self, scenario_id: Union[int, str], scenario: ScenarioIn, response: Response, dataset_id: Union[int, str]):
        """
        Create scenario in database
        """
        create_response = self.scenario_service.add_scenario_execution(scenario_id, scenario, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post(
        "/scenarios/add_activity_execution/{previous_id}",
        tags=["scenarios"],
        response_model=ActivityExecutionOut,
    )
    async def add_activity_execution(
            self,
            previous_id: Union[int, str],
            activity_execution: ActivityExecutionIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Add new activity execution to scenario
        """
        create_response = self.scenario_service.add_activity_execution(
            previous_id, activity_execution, dataset_id
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.put("/scenarios", tags=["scenarios"], response_model=OrderChangeOut)
    async def change_order(self, order_change: OrderChangeIn, response: Response, dataset_id: Union[int, str]):
        """
        Change order of one activity execution in scenario
        """
        put_response = self.scenario_service.change_order(order_change, dataset_id)
        if put_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        put_response.links = get_links(router)

        return put_response

    @router.put("/scenarios/{scenario_id}", tags=["scenarios"], response_model=Union[ScenarioOut, NotFoundByIdModel])
    async def update_scenario(self, scenario_id: Union[int, str], scenario: ScenarioIn, response: Response, dataset_id: Union[int, str]):
        """
        Change order of one activity execution in scenario
        """
        update_response = self.scenario_service.update_scenario(scenario_id, scenario, dataset_id)
        if update_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.delete(
        "/scenarios/{scenario_execution_id}",
        tags=["scenarios"],
        response_model=ScenarioOut,
    )
    async def delete_scenario_execution(
            self, scenario_execution_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete activity execution from scenario
        """
        delete_response = self.scenario_service.delete_scenario_execution(
            scenario_execution_id, dataset_id
        )
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response


    @router.delete(
        "/scenarios/delete_activity_execution/{activity_execution_id}",
        tags=["scenarios"],
        response_model=ActivityExecutionOut,
    )
    async def delete_activity_execution(
            self, activity_execution_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete activity execution from scenario
        """
        delete_response = self.scenario_service.delete_activity_execution(
            activity_execution_id, dataset_id
        )
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response

    @router.get(
        "/scenarios/{node_id}",
        tags=["scenarios"],
        response_model=Union[ScenarioOut, NotFoundByIdModel],
    )
    async def get_scenario(
            self, node_id: Union[int, str], depth: int, response: Response, dataset_id: Union[int, str]
    ):
        """
        Get scenario from database. Depth attribute specifies how many models will be traversed to create the response.
        """
        get_response = self.scenario_service.get_scenario(node_id, dataset_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
