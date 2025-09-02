from typing import Union
from uuid import uuid4

from fastapi import Response, Depends, UploadFile, File
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from grisera.clients.minio_client import MinIOClient
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.registered_data.registered_data_model import (
    RegisteredDataIn,
    RegisteredDataOut,
    RegisteredDataNodesOut,
)
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class RegisteredDataRouter:
    """
    Class for routing registered data based requests

    Attributes:
        registered_data_service (RegisteredDataService): Service instance for registered data
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.registered_data_service = service_factory.get_registered_data_service()
        self.minio_client = MinIOClient("recordings")

    @router.post("/registered-data/upload-file", tags=["upload"])
    async def upload_file(self, response: Response, file: UploadFile = File(...)):
        """
        Upload a file associated with a recording and store it in MinIO S3 storage
        """
        try:
            # Read file content
            file_content = await file.read()
            
            # Generate unique object name
            uuid = uuid4()
            object_name = f"{uuid}/{file.filename}"
            
            # Upload using our MinIO client (configured for recordings bucket)
            self.minio_client.upload_file(object_name, file_content, file.content_type)
            
            # Add HATEOAS links
            links = get_links(router)
            
            response.status_code = 200
            return {
                "message": "File uploaded successfully",
                "object_name": object_name,  # Store object name instead of public URL
                "uuid": str(uuid),
                "filename": file.filename,
                "links": links,
            }
        except Exception as e:
            response.status_code = 500
            return {"error": f"Failed to upload file: {str(e)}"}

    @router.get("/registered-data/preview/{object_name:path}", tags=["upload"])
    def get_preview_url(self, object_name: str, response: Response):
        """
        Generate pre-signed URL for previewing recording file
        
        Args:
            object_name (str): Object name in MinIO (uuid/filename format)
            
        Returns:
            Dict: Pre-signed preview URL and metadata
        """
        try:
            # Extract filename for content type detection
            filename = object_name.split('/')[-1] if '/' in object_name else object_name
            
            # Import here to avoid circular imports
            from grisera.file.file_validation import FileValidator
            validator = FileValidator()
            content_type = validator.get_content_type(filename)
            
            if not validator.is_previewable(content_type):
                response.status_code = 400
                return {"error": "Preview not available for this file type"}
            
            preview_info = self.minio_client.generate_preview_url(
                object_name, 
                content_type
            )
            
            response.status_code = 200
            return preview_info
        except Exception as e:
            response.status_code = 500
            return {"error": f"Failed to generate preview URL: {str(e)}"}

    @router.post(
        "/registered_data", tags=["registered data"], response_model=RegisteredDataOut
    )
    async def create_registered_data(
            self, registered_data: RegisteredDataIn, response: Response, dataset_id: Union[int, str]
    ):
        """
        Create registered data in database
        """
        create_response = self.registered_data_service.save_registered_data(
            registered_data, dataset_id
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def get_registered_data(
            self, registered_data_id: Union[int, str], response: Response, dataset_id: Union[int, str], depth: int = 0
    ):
        """
        Get registered data from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.registered_data_service.get_registered_data(
            registered_data_id, dataset_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/registered_data",
        tags=["registered data"],
        response_model=RegisteredDataNodesOut,
    )
    async def get_registered_data_nodes(self, response: Response, dataset_id: Union[int, str]):
        """
        Get registered data from database
        """

        get_response = self.registered_data_service.get_registered_data_nodes(dataset_id)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def delete_registered_data(
            self, registered_data_id: Union[int, str], response: Response, dataset_id: Union[int, str]
    ):
        """
        Delete registered data from database
        """
        get_response = self.registered_data_service.delete_registered_data(
            registered_data_id, dataset_id
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/registered_data/{registered_data_id}",
        tags=["registered data"],
        response_model=Union[RegisteredDataOut, NotFoundByIdModel],
    )
    async def update_registered_data(
            self,
            registered_data_id: Union[int, str],
            registered_data: RegisteredDataIn,
            response: Response, dataset_id: Union[int, str]
    ):
        """
        Update registered data model in database
        """
        update_response = self.registered_data_service.update_registered_data(
            registered_data_id, registered_data, dataset_id
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
