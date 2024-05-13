from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.participant_state.participant_state_model import (
    ParticipantStateIn,
    ParticipantStatesOut,
    ParticipantStateOut,
    ParticipantStatePropertyIn,
    ParticipantStateRelationIn,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class ParticipantStateRouter:
    """
    Class for routing participant state based requests

    Attributes:
        participant_state_service (ParticipantStateService): Service instance for participants' states
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.participant_state_service = service_factory.get_participant_state_service()

    @router.post(
        "/participant_state",
        tags=["participant state"],
        response_model=ParticipantStateOut,
    )
    async def create_participant_state(
            self, participant_state: ParticipantStateIn, response: Response, dataset_name: str
    ):
        """
        Create participant state in database
        """

        create_response = self.participant_state_service.save_participant_state(
            participant_state, dataset_name
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/participant_state",
        tags=["participant state"],
        response_model=ParticipantStatesOut,
    )
    async def get_participant_states(self, response: Response, dataset_name: str):
        """
        Get participant states from database
        """

        get_response = self.participant_state_service.get_participant_states(dataset_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def get_participant_state(
            self, participant_id: Union[int, str], response: Response, dataset_name: str, depth: int = 0
    ):
        """
        Get participant state from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.participant_state_service.get_participant_state(
            participant_id, dataset_name, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def delete_participant_state(
            self, participant_state_id: Union[int, str], response: Response, dataset_name: str
    ):
        """
        Delete participant state from database
        """
        get_response = self.participant_state_service.delete_participant_state(
            participant_state_id, dataset_name
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def update_participant_state(
            self,
            participant_state_id: Union[int, str],
            participant_state: ParticipantStatePropertyIn,
            response: Response,
            dataset_name: str
    ):
        """
        Update participant state model in database
        """
        update_response = self.participant_state_service.update_participant_state(
            participant_state_id, participant_state, dataset_name
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/participant_state/{participant_state_id}/relationships",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def update_participant_state_relationships(
            self,
            participant_state_id: Union[int, str],
            participant_state: ParticipantStateRelationIn,
            response: Response,
            dataset_name: str
    ):
        """
        Update participant state relations in database
        """
        update_response = (
            self.participant_state_service.update_participant_state_relationships(
                participant_state_id, participant_state, dataset_name
            )
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
