from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel

from grisera.models.base_model_out import BaseModelOut


class FileIn(BaseModel):
    """
    Model of file to acquire from client

    Attributes:
        filename (Optional[str]): Generated filename in storage
        original_filename (Optional[str]): Original filename uploaded by user
        name (Optional[str]): Custom name given by user
        size (Optional[int]): File size in bytes
        content_type (Optional[str]): MIME type of the file
        dataset_id (Union[int, str]): ID of associated dataset (required)
    """

    filename: Optional[str]
    original_filename: Optional[str]
    name: Optional[str]
    size: Optional[int]
    content_type: Optional[str]
    dataset_id: Union[int, str]


class BasicFileOut(FileIn):
    """
    Model of file

    Attributes:
        id (Optional[int | str]): Id of file returned from api
        uploaded_at (Optional[datetime]): Upload timestamp
    """
    id: Optional[Union[int, str]]
    uploaded_at: Optional[datetime]


class FileOut(BasicFileOut, BaseModelOut):
    """
    Model of file to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """


class FilesOut(BaseModelOut):
    """
    Model of list of files

    Attributes:
        files (Optional[List[BasicFileOut]]): List of files to send
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    files: Optional[List[BasicFileOut]]