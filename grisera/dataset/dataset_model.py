from datetime import date
from typing import Optional, List, Union

from pydantic import BaseModel

from grisera.property.property_model import PropertyIn
from grisera.models.base_model_out import BaseModelOut


class DatasetIn(BaseModel):
    """
        Model of dataset to acquire from client

        Attributes:
            name (Optional[str]): Name of the dataset given by user
            creator (Optional[str]): Creator of the dataset given by user
            date (Optional[date]): Date of the dataset given by user
            description (Optional[date]): Description of the dataset given by user
            additional_properties (Optional[List[PropertyIn]]): Additional properties for dataset
    """

    name: Optional[str]
    creator: Optional[str]
    date: Optional[date]
    description: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class BasicDatasetOut(DatasetIn):
    """
        Model of dataset

        Attributes:
            id (Optional[int | str]): Id of dataset returned from api
            rights (Optional[str]): Rights set to the dataset given by user
    """
    id: Optional[Union[int, str]]
    rights: Optional[str]


class DatasetOut(BasicDatasetOut, BaseModelOut):
    """
        Model of dataset to send to client as a result of request

        Attributes:
            errors (Optional[Any]): Optional errors appeared during query executions
            links (Optional[list): Hateoas implementation
    """


class DatasetsOut(BaseModelOut):
    """
    Model of list of datasets

    Attributes:
        datasets (Optional[List[BasicDatasetOut]]): List of datasets to send
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    datasets: Optional[List[BasicDatasetOut]]
