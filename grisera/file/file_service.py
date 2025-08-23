from datetime import datetime
from typing import Union, Optional, Dict, Any

from grisera.file.file_model import BasicFileOut


class FileService:
    """
    Object to handle logic of files requests

    Attributes:
        files_storage (dict): In-memory storage for files metadata
    """

    def __init__(self):
        self.files_storage = {}

    def save_file_metadata(self, filename: str, original_filename: str, name: str, size: int, 
                          content_type: str, dataset_id: Union[int, str]) -> BasicFileOut:
        """
        Save file metadata

        Args:
            filename (str): Generated filename in storage
            original_filename (str): Original filename
            name (str): Custom name given by user
            size (int): File size
            content_type (str): MIME type
            dataset_id (Union[int, str]): Associated dataset ID

        Returns:
            BasicFileOut: Created file metadata
        """
        file_id = str(len(self.files_storage) + 1)
        file_data = BasicFileOut(
            id=file_id,
            filename=filename,
            original_filename=original_filename,
            name=name,
            size=size,
            content_type=content_type,
            dataset_id=dataset_id,
            uploaded_at=datetime.utcnow()
        )
        self.files_storage[file_id] = file_data
        return file_data

    def get_files(self) -> list:
        """
        Get all files

        Returns:
            list: List of all files
        """
        return list(self.files_storage.values())

    def get_files_by_dataset(self, dataset_id: Union[int, str]) -> list:
        """
        Get files filtered by dataset ID

        Args:
            dataset_id (Union[int, str]): Dataset ID

        Returns:
            list: List of files for the dataset
        """
        return [file for file in self.files_storage.values() if str(file.dataset_id) == str(dataset_id)]

    def get_file_by_id(self, file_id: Union[int, str]) -> Optional[BasicFileOut]:
        """
        Get file by ID

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            Optional[BasicFileOut]: File metadata if found
        """
        return self.files_storage.get(str(file_id))

    def delete_file(self, file_id: Union[int, str]) -> bool:
        """
        Delete file metadata

        Args:
            file_id (Union[int, str]): File ID

        Returns:
            bool: True if deleted, False if not found
        """
        file_key = str(file_id)
        if file_key in self.files_storage:
            del self.files_storage[file_key]
            return True
        return False