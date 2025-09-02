from typing import Union, List

from fastapi import Response, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from grisera.clients.minio_client import MinIOClient
from grisera.file.file_model import FileOut, FilesOut
from grisera.file.file_service import FileService
from grisera.file.file_validation import FileValidator
from grisera.file.upload_handler import UploadHandler
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
        self.minio_client = MinIOClient("files")
        self.validator = FileValidator()
        self.upload_handler = UploadHandler(self.file_service, router)

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

    @router.post("/files/upload", tags=["files"], response_model=Union[FileOut, List[FileOut]])
    async def upload_file(self, response: Response, file: UploadFile = File(...), 
                         name: str = Form(...), dataset_id: str = Form(...)) -> Union[FileOut, List[FileOut]]:
        """
        Upload a file and store it in MinIO S3 storage.
        If the file is a ZIP archive, it will be extracted and each file uploaded separately.

        Args:
            file (UploadFile): File to upload
            name (str): Custom name given by user (form field, required)
            dataset_id (str): Associated dataset ID (form field, required)

        Returns:
            Union[FileOut, List[FileOut]]: File metadata or list of extracted files metadata
        """
        try:
            result = await self.upload_handler.handle_upload(file, name, dataset_id)
            response.status_code = 201
            return result
        except HTTPException:
            raise
        except Exception as e:
            response.status_code = 500
            raise HTTPException(status_code=500, detail=f"Unexpected error during file upload: {str(e)}")

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
        
        try:
            download_info = self.minio_client.generate_download_url(
                file_data.filename, 
                file_data.original_filename
            )
            
            response.status_code = 200
            return download_info
        except HTTPException:
            raise

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
        
        if not self.validator.is_previewable(file_data.content_type):
            raise HTTPException(status_code=400, detail="Preview not available for this file type")
        
        try:
            file_response = self.minio_client.get_file(file_data.filename)
            
            # Headers for optimized streaming of large files
            headers = {
                "Content-Length": str(file_data.size),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600",  # Allow caching for preview
            }
            
            return StreamingResponse(
                file_response, 
                media_type=file_data.content_type,
                headers=headers
            )
        except HTTPException:
            raise

    @router.get("/files/{file_id}/preview-url", tags=["files"])
    def get_preview_url(self, file_id: Union[int, str], response: Response):
        """
        Generate pre-signed URL for file preview in browser

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            Dict: Pre-signed preview URL
        """
        file_data = self.file_service.get_file_by_id(file_id)
        
        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found")
        
        if not self.validator.is_previewable(file_data.content_type):
            raise HTTPException(status_code=400, detail="Preview not available for this file type")
        
        try:
            preview_info = self.minio_client.generate_preview_url(
                file_data.filename, 
                file_data.content_type
            )
            
            response.status_code = 200
            return preview_info
        except HTTPException:
            raise

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
        
        try:
            # Delete from MinIO
            self.minio_client.delete_file(file_data.filename)
            
            # Delete metadata
            self.file_service.delete_file(file_id)
            
            response.status_code = 200
            return {"message": "File deleted successfully", "links": get_links(router)}
            
        except HTTPException:
            raise