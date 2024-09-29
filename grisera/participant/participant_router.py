from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.participant.participant_model import (
    ParticipantIn,
    ParticipantOut,
    ParticipantsOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class ParticipantRouter:
    """
    Class for routing participant based requests

    Attributes:
        participant_service (ParticipantService): Service instance for participants
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.participant_service = service_factory.get_participant_service()

    @router.post("/participants", tags=["participants"], response_model=ParticipantOut)
    async def create_participant(self, participant: ParticipantIn, response: Response, dataset_id: Union[int, str]):
        """
        Create participant in database
        """

        if participant.date_of_birth is not None:
            participant.date_of_birth = participant.date_of_birth.__str__()

        create_response = self.participant_service.save_participant(participant, dataset_id)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/participants", tags=["participants"], response_model=ParticipantsOut)
    async def get_participants(self, response: Response, dataset_id: Union[int, str]):
        """
        Get participants from database
        """

        get_response = self.participant_service.get_participants(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def get_participant(
            self, participant_id: Union[str, int], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get participant from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.participant_service.get_participant(participant_id, dataset_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def delete_participant(
            self, participant_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete participant from database
        """
        get_response = self.participant_service.delete_participant(participant_id, dataset_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def update_participant(
            self,
            participant_id: Union[int, str],
            participant: ParticipantIn,
            response: Response,
            dataset_id: Union[int, str]
    ):
        """
        Update participant model in database
        """
        update_response = self.participant_service.update_participant(
            participant_id, participant, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
