from fastapi import Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.dataset.dataset_model import DatasetIn, DatasetOut, DatasetsOut
from grisera.helpers.hateoas import get_links
from grisera.models.not_found_model import NotFoundByIdModel
from typing import Union
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory
import time

from grisera.modality.modality_model import ModalityIn
from grisera.modality.modality_model import Modality as modality_types
from grisera.life_activity.life_activity_model import LifeActivityIn
from grisera.life_activity.life_activity_model import LifeActivity as life_activity_types
from grisera.channel.channel_model import ChannelIn
from grisera.channel.channel_model import Type as channel_types
router = InferringRouter()


@cbv(router)
class DatasetRouter:
    """
    Class for routing dataset based requests

    Attributes:
        dataset_service (DatasetService): Service instance for datasets
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.dataset_service = service_factory.get_dataset_service()
        self.channel_service = service_factory.get_channel_service()
        self.modality_service = service_factory.get_modality_service()
        self.life_activity_service = service_factory.get_life_activity_service()

    @router.post("/datasets", tags=["datasets"], response_model=DatasetOut)
    async def create_dataset(self, response: Response, dataset_name_from_user: str):
        """
        Create dataset with given name
        """
        create_dataset_response = self.dataset_service.save_dataset(dataset_name_from_user)
        if create_dataset_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_dataset_response.links = get_links(router)

        # wait for the dataset to be created
        time.sleep(0.5)

        # create channels nodes for the dataset
        for channel_type in channel_types:
            create_channel_response = self.channel_service.save_channel(ChannelIn(type=channel_type.value), create_dataset_response.name_hash)

        # create modalities nodes for the dataset
        for modality_type in modality_types:
            create_modality_response = self.modality_service.save_modality(ModalityIn(modality=modality_type.value), create_dataset_response.name_hash)

        # create life activities nodes for the dataset
        for life_activity_type in life_activity_types:
            create_life_activity_response = self.life_activity_service.save_life_activity(LifeActivityIn(life_activity=life_activity_type.value), create_dataset_response.name_hash)

        return create_dataset_response

    @router.get("/datasets/{database_name}", tags=["datasets"], response_model=Union[DatasetOut, NotFoundByIdModel])
    async def get_dataset(self, response: Response, dataset_name: str):
        """
        Get dataset by name
        """

        get_response = self.dataset_service.get_dataset(dataset_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/datasets", tags=["datasets"], response_model=DatasetsOut)
    async def get_datasets(self, response: Response):
        """
        Get all datasets
        """
        get_response = self.dataset_service.get_datasets()
        if get_response.errors is not None:
            response.status_code = 422

        get_response.links = get_links(router)

        return get_response

    @router.delete("/datasets/{database_name}", tags=["datasets"], response_model=Union[DatasetOut, NotFoundByIdModel])
    async def delete_dataset(self, response: Response, dataset_name: str):
        """
        Delete dataset by name
        """
        delete_response = self.dataset_service.delete_dataset(dataset_name)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response
