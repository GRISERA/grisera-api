from typing import List, Union
from uuid import uuid4

from fastapi import UploadFile, HTTPException

from grisera.clients.minio_client import MinIOClient
from grisera.file.archive_extractor import ArchiveExtractor
from grisera.file.file_validation import FileValidator
from grisera.file.file_model import FileOut
from grisera.file.file_service import FileService
from grisera.helpers.hateoas import get_links


class UploadHandler:
    """
    Main handler for file upload operations
    """
    
    def __init__(self, file_service: FileService, router=None):
        self.file_service = file_service
        self.router = router
        self.validator = FileValidator()
        self.minio_client = MinIOClient("files")
        self.archive_extractor = ArchiveExtractor()
    
    async def handle_upload(self, file: UploadFile, name: str, 
                          dataset_id: str) -> Union[FileOut, List[FileOut]]:
        """
        Handle file upload with support for archives
        
        Args:
            file (UploadFile): Uploaded file
            name (str): Custom name for the file
            dataset_id (str): Associated dataset ID
            
        Returns:
            Union[FileOut, List[FileOut]]: Single file or list of extracted files
        """
        # Validate input parameters
        self._validate_upload_params(file, name, dataset_id)
        
        # Read file content
        file_content = await file.read()
        
        # Validate file
        self.validator.validate_file_upload(file.filename, file_content, file.content_type)
        
        # Check if file is an archive
        is_archive, archive_type = self.validator.is_archive_file(file.filename, file.content_type)
        
        if is_archive:
            return await self._handle_archive_upload(file_content, file.filename, 
                                                   file.content_type, name, dataset_id)
        else:
            return await self._handle_single_file_upload(file_content, file.filename, 
                                                       file.content_type, name, dataset_id)
    
    def _validate_upload_params(self, file: UploadFile, name: str, dataset_id: str) -> None:
        """Validate upload parameters"""
        if not name or name.strip() == '':
            raise HTTPException(status_code=400, detail="File name is required")
        
        if not dataset_id or dataset_id.strip() == '':
            raise HTTPException(status_code=400, detail="Dataset ID is required")
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
    
    async def _handle_single_file_upload(self, file_content: bytes, filename: str, 
                                       content_type: str, name: str, 
                                       dataset_id: str) -> FileOut:
        """Handle upload of a single file"""
        base_uuid = str(uuid4())
        
        # Use custom name for display path if provided, otherwise use original filename
        display_path = name if name else filename
        
        return self._upload_single_file(
            file_content=file_content,
            original_filename=filename,
            display_path=display_path,
            base_uuid=base_uuid,
            custom_name=name,
            dataset_id=dataset_id,
            content_type=content_type
        )
    
    async def _handle_archive_upload(self, file_content: bytes, filename: str, 
                                   content_type: str, name: str, 
                                   dataset_id: str) -> List[FileOut]:
        """Handle upload and extraction of archive files"""
        # Extract archive
        extracted_files = self.archive_extractor.extract_archive(
            content=file_content,
            filename=filename,
            content_type=content_type
        )
        
        if not extracted_files:
            raise HTTPException(status_code=400, detail="No valid files found in archive")
        
        # Upload all extracted files
        uploaded_files = []
        base_uuid = str(uuid4())
        
        for file_data, original_filename, display_path in extracted_files:
            # Get content type for extracted file
            extracted_content_type = self.validator.get_content_type(original_filename)
            
            uploaded_file = self._upload_single_file(
                file_content=file_data,
                original_filename=original_filename,
                display_path=display_path,
                base_uuid=base_uuid,
                custom_name=f"{name}/{display_path}",
                dataset_id=dataset_id,
                content_type=extracted_content_type
            )
            uploaded_files.append(uploaded_file)
        
        return uploaded_files
    
    def _upload_single_file(self, file_content: bytes, original_filename: str, 
                          display_path: str, base_uuid: str, custom_name: str,
                          dataset_id: str, content_type: str = None) -> FileOut:
        """
        Upload a single file to storage and save metadata
        
        Args:
            file_content (bytes): File content
            original_filename (str): Original filename
            display_path (str): Display path for the file
            base_uuid (str): Base UUID for storage organization
            custom_name (str): Custom name for display
            dataset_id (str): Dataset ID
            content_type (str): MIME type
            
        Returns:
            FileOut: File metadata with links
        """
        # Generate object name for storage
        object_name = f"{base_uuid}/{display_path}"
        
        # Determine content type if not provided
        if not content_type:
            content_type = self.validator.get_content_type(original_filename)
        
        # Upload to MinIO
        self.minio_client.upload_file(object_name, file_content, content_type)
        
        # Save file metadata
        file_metadata = self.file_service.save_file_metadata(
            filename=object_name,
            original_filename=original_filename,
            name=custom_name,
            size=len(file_content),
            content_type=content_type,
            dataset_id=dataset_id
        )
        
        # Return with HATEOAS links
        return FileOut(
            **file_metadata.dict(),
            links=get_links(self.router) if self.router else []
        )