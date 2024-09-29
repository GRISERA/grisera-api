from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.experiment.experiment_model import ExperimentIn, ExperimentOut, ExperimentsOut
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ExperimentRouter:
    """
    Class for routing experiment based requests

    Attributes:
        experiment_service (ExperimentService): Service instance for experiments
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.experiment_service = service_factory.get_experiment_service()

    @router.post("/experiments", tags=["experiments"], response_model=ExperimentOut)
    async def create_experiment(self, experiment: ExperimentIn, response: Response, dataset_id: Union[int, str]):
        """
        Create experiment in database
        """
        create_response = self.experiment_service.save_experiment(experiment, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/experiments/{experiment_id}",
        tags=["experiments"],
        response_model=Union[ExperimentOut, NotFoundByIdModel],
    )
    async def get_experiment(
            self, experiment_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):

        """
        Get experiment from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.experiment_service.get_experiment(experiment_id, dataset_id, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/experiments", tags=["experiments"], response_model=ExperimentsOut)
    async def get_experiments(self, response: Response, dataset_id: Union[int, str]):
        """
        Get experiments from database
        """

        get_response = self.experiment_service.get_experiments(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/experiments/{experiment_id}",
        tags=["experiments"],
        response_model=Union[ExperimentOut, NotFoundByIdModel],
    )
    async def delete_experiment(
            self, experiment_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):

        """
        Delete experiment from database
        """
        get_response = self.experiment_service.delete_experiment(experiment_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/experiments/{experiment_id}",
        tags=["experiments"],
        response_model=Union[ExperimentOut, NotFoundByIdModel],
    )
    async def update_experiment(
            self,
            experiment_id: Union[int, str],
            experiment: ExperimentIn,
            response: Response,
            dataset_id: Union[int, str]
    ):
        """
        Update experiment model in database
        """
        update_response = self.experiment_service.update_experiment(
            experiment_id, experiment, dataset_id
        )

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
