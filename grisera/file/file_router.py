import os
import io
from typing import Union
from uuid import uuid4

from fastapi import Response, Depends, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from minio import Minio
from minio.error import S3Error

from grisera.auth.auth_bearer import JWTBearer
from grisera.file.file_model import FileOut, FilesOut
from grisera.file.file_service import FileService
from grisera.helpers.hateoas import get_links
from grisera.helpers.helpers import check_dataset_permission
from grisera.models.not_found_model import NotFoundByIdModel
from grisera.services.service import service
from grisera.services.service_factory import ServiceFactory

router = InferringRouter(dependencies=[Depends(check_dataset_permission)])


@cbv(router)
class FileRouter:
    """
    Class for routing file based requests
    
    Attributes:
        file_service (FileService): Service instance for files
    """

    def __init__(self, service_factory: ServiceFactory = Depends(service.get_service_factory)):
        self.file_service = service_factory.get_file_service()

    @router.get("/files", tags=["files"], response_model=FilesOut)
    def get_files(self, response: Response, dataset_id: Union[int, str]) -> FilesOut:
        """
        Get all files metadata for a specific dataset

        Args:
            dataset_id (Union[int, str]): Dataset ID to filter files

        Returns:
            FilesOut: List of files with metadata filtered by dataset
        """
        files = self.file_service.get_files_by_dataset(dataset_id)
        response.status_code = 200

        return FilesOut(
            files=files,
            links=get_links(router)
        )

    @router.get("/files/{file_id}", tags=["files"], response_model=Union[FileOut, NotFoundByIdModel])
    def get_file(self, file_id: Union[int, str], response: Response) -> Union[FileOut, NotFoundByIdModel]:
        """
        Get file metadata by ID

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            Union[FileOut, NotFoundByIdModel]: File metadata or not found response
        """
        file_data = self.file_service.get_file_by_id(file_id)
        
        if file_data is None:
            response.status_code = 404
            return NotFoundByIdModel(id=file_id, errors="File not found")

        response.status_code = 200
        return FileOut(
            **file_data.dict(),
            links=get_links(router)
        )

    @router.post("/files/upload", tags=["files"], response_model=FileOut)
    async def upload_file(self, response: Response, file: UploadFile = File(...), 
                         name: str = Form(...), dataset_id: str = Form(...)) -> FileOut:
        """
        Upload a file and store it in MinIO S3 storage

        Args:
            file (UploadFile): File to upload
            name (str): Custom name given by user (form field, required)
            dataset_id (str): Associated dataset ID (form field, required)

        Returns:
            FileOut: File metadata
        """
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "us-east-1")
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "s3:9000")

        minio_client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            region=region,
        )

        uuid = uuid4()
        bucket_name = "files"
        object_name = f"{uuid}/{file.filename}"

        try:
            if not minio_client.bucket_exists(bucket_name):
                minio_client.make_bucket(bucket_name)

            file_content = await file.read()
            file_stream = io.BytesIO(file_content)
            
            minio_client.put_object(
                bucket_name,
                object_name,
                file_stream,
                length=len(file_content),
                content_type=file.content_type,
            )

            # Save file metadata
            if not name:
                response.status_code = 400
                raise HTTPException(status_code=400, detail="File name is required")
            
            if not dataset_id:
                response.status_code = 400
                raise HTTPException(status_code=400, detail="Dataset ID is required")
                
            file_metadata = self.file_service.save_file_metadata(
                filename=object_name,
                original_filename=file.filename,
                name=name,
                size=len(file_content),
                content_type=file.content_type,
                dataset_id=dataset_id
            )

            response.status_code = 201
            return FileOut(
                **file_metadata.dict(),
                links=get_links(router)
            )

        except S3Error as e:
            response.status_code = 500
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    @router.get("/files/{file_id}/download", tags=["files"])
    def download_file(self, file_id: Union[int, str], response: Response):
        """
        Generate pre-signed URL for direct download from MinIO storage

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            Dict: Pre-signed download URL
        """
        file_data = self.file_service.get_file_by_id(file_id)
        
        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found")

        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "us-east-1")
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "s3:9000")

        minio_client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            region=region,
        )

        bucket_name = "files"
        
        try:
            from datetime import timedelta
            
            # For public URLs, create a separate client with public endpoint
            public_minio_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT", "localhost:9000")
            public_minio_client = Minio(
                public_minio_endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=False,
                region=region,
            )
            
            # Generate pre-signed URL valid for 1 hour using public endpoint
            download_url = public_minio_client.presigned_get_object(
                bucket_name, 
                file_data.filename,
                expires=timedelta(hours=1),
                response_headers={
                    'response-content-disposition': f'attachment; filename="{file_data.original_filename}"'
                }
            )
            
            response.status_code = 200
            return {
                "download_url": download_url,
                "filename": file_data.original_filename,
                "expires_in": 3600  # 1 hour in seconds
            }
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")

    @router.get("/files/{file_id}/preview", tags=["files"])
    def preview_file(self, file_id: Union[int, str]):
        """
        Preview file content (for text and image files)

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            File content for preview
        """
        file_data = self.file_service.get_file_by_id(file_id)
        
        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found")

        # Allow preview for common previewable file types
        previewable_types = [
            'text/',           # Text files
            'image/',          # Images
            'application/pdf', # PDF files
            'application/json',# JSON files
            'application/xml', # XML files
            'video/',          # Video files
            'audio/',          # Audio files
        ]
        
        is_previewable = any(file_data.content_type.startswith(ptype) or 
                           file_data.content_type == ptype 
                           for ptype in previewable_types)
        
        if not is_previewable:
            raise HTTPException(status_code=400, detail="Preview not available for this file type")

        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "us-east-1")
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "s3:9000")

        minio_client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            region=region,
        )

        bucket_name = "files"
        
        try:
            response = minio_client.get_object(bucket_name, file_data.filename)
            
            # Headers for optimized streaming of large files
            headers = {
                "Content-Length": str(file_data.size),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600",  # Allow caching for preview
            }
            
            return StreamingResponse(
                response, 
                media_type=file_data.content_type,
                headers=headers
            )
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to preview file: {str(e)}")

    @router.delete("/files/{file_id}", tags=["files"])
    def delete_file(self, file_id: Union[int, str], response: Response):
        """
        Delete file and its metadata

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            Dict with success message
        """
        file_data = self.file_service.get_file_by_id(file_id)
        
        if file_data is None:
            response.status_code = 404
            return NotFoundByIdModel(id=file_id, errors="File not found")

        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "us-east-1")
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "s3:9000")

        minio_client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            region=region,
        )

        bucket_name = "files"
        
        try:
            # Delete from MinIO
            minio_client.remove_object(bucket_name, file_data.filename)
            
            # Delete metadata
            self.file_service.delete_file(file_id)
            
            response.status_code = 200
            return {"message": "File deleted successfully", "links": get_links(router)}
            
        except S3Error as e:
            response.status_code = 500
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")