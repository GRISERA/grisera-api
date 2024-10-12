from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.participation.participation_model import (
    ParticipationIn,
    ParticipationOut,
    ParticipationsOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ParticipationRouter:
    """
    Class for routing participation based requests

    Attributes:
        participation_service (ParticipationService): Service instance for participation
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.participation_service = service_factory.get_participation_service()

    @router.post(
        "/participations", tags=["participations"], response_model=ParticipationOut
    )
    async def create_participation(
            self, participation: ParticipationIn, response: Response, dataset_id: Union[int, str]
    ):
        """
        Create participation in database
        """
        create_response = self.participation_service.save_participation(participation, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/participations", tags=["participations"], response_model=ParticipationsOut
    )
    async def get_participations(self, response: Response, dataset_id: Union[int, str]):
        """
        Get participations from database
        """

        get_response = self.participation_service.get_participations(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/participations/{participation_id}",
        tags=["participations"],
        response_model=Union[ParticipationOut, NotFoundByIdModel],
    )
    async def get_participation(
            self, participation_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get participation from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.participation_service.get_participation(
            participation_id, dataset_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/participations/{participation_id}",
        tags=["participations"],
        response_model=Union[ParticipationOut, NotFoundByIdModel],
    )
    async def delete_participation(
            self, participation_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):

        """
        Delete participations from database
        """
        get_response = self.participation_service.delete_participation(participation_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/participations/{participation_id}/relationships",
        tags=["participations"],
        response_model=Union[ParticipationOut, NotFoundByIdModel],
    )
    async def update_participation_relationships(
            self,
            participation_id: Union[int, str],
            participation: ParticipationIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update participations relations in database
        """
        update_response = self.participation_service.update_participation_relationships(
            participation_id, participation, dataset_id
        )

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
