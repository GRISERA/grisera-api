from typing import Union

from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.helpers.hateoas import get_links
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.recording.recording_model import (
    RecordingPropertyIn,
    RecordingRelationIn,
    RecordingIn,
    RecordingOut,
    RecordingsOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter()


@cbv(router)
class RecordingRouter:
    """
    Class for routing recording based requests

    Attributes:
        recording_service (RecordingService): Service instance for recording
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.recording_service = service_factory.get_recording_service()

    @router.post("/recordings", tags=["recordings"], response_model=RecordingOut)
    async def create_recording(self, recording: RecordingIn, response: Response):
        """
        Create Recording in database
        """
        create_response = self.recording_service.save_recording(recording)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/recordings", tags=["recordings"], response_model=RecordingsOut)
    async def get_recordings(self, response: Response):
        """
        Get recordings from database
        """

        get_response = self.recording_service.get_recordings()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/recordings/{recording_id}",
        tags=["recordings"],
        response_model=Union[RecordingOut, NotFoundByIdModel],
    )
    async def get_recording(
        self, recording_id: Union[int, str], response: Response, depth: int=0
    ):
        """
        Get recordings from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.recording_service.get_recording(recording_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/recordings/{recording_id}",
        tags=["recordings"],
        response_model=Union[RecordingOut, NotFoundByIdModel],
    )
    async def delete_recording(self, recording_id: Union[int, str], response: Response):
        """
        Delete recordings from database
        """
        get_response = self.recording_service.delete_recording(recording_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/recordings/{recording_id}",
        tags=["recordings"],
        response_model=Union[RecordingOut, NotFoundByIdModel],
    )
    async def update_recording(
        self,
        recording_id: Union[int, str],
        recording: RecordingPropertyIn,
        response: Response,
    ):
        """
        Update recording model in database
        """
        update_response = self.recording_service.update_recording(
            recording_id, recording
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/recordings/{recording_id}/relationships",
        tags=["recordings"],
        response_model=Union[RecordingOut, NotFoundByIdModel],
    )
    async def update_recording_relationships(
        self,
        recording_id: Union[int, str],
        recording: RecordingRelationIn,
        response: Response,
    ):
        """
        Update recordings relations in database
        """
        update_response = self.recording_service.update_recording_relationships(
            recording_id, recording
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
