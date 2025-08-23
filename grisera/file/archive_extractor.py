import io
import gzip
import zipfile
import tarfile
from typing import List, Tuple, Generator
from uuid import uuid4

from fastapi import HTTPException

from grisera.file.file_validation import FileValidator


class ArchiveExtractor:
    """
    Service for extracting various archive formats with recursive support
    """
    
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.validator = FileValidator()
    
    def extract_archive(self, content: bytes, filename: str, content_type: str = None, 
                       base_path: str = "", base_uuid: str = None, 
                       current_depth: int = 0) -> List[Tuple[bytes, str, str]]:
        """
        Extract archive with recursive support
        
        Args:
            content (bytes): Archive content
            filename (str): Archive filename
            content_type (str): MIME type
            base_path (str): Base path for extracted files
            base_uuid (str): UUID for organization
            current_depth (int): Current recursion depth
            
        Returns:
            List of tuples: (file_content, original_filename, display_path)
        """
        if current_depth >= self.max_depth:
            raise HTTPException(status_code=400, detail="Maximum archive nesting depth exceeded")
        
        if base_uuid is None:
            base_uuid = str(uuid4())
        
        is_archive, archive_type = self.validator.is_archive_file(filename, content_type)
        
        if not is_archive:
            raise HTTPException(status_code=400, detail=f"File is not a supported archive: {filename}")
        
        if archive_type == 'zip':
            return self._extract_zip(content, base_path, base_uuid, current_depth)
        elif archive_type in ['tar', 'tar.gz']:
            return self._extract_tar(content, base_path, base_uuid, current_depth)
        elif archive_type == 'gz':
            return self._extract_gz(content, base_path, base_uuid, current_depth)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported archive type: {archive_type}")
    
    def _extract_zip(self, zip_content: bytes, base_path: str, base_uuid: str, 
                    current_depth: int) -> List[Tuple[bytes, str, str]]:
        """Extract ZIP archive recursively"""
        extracted_files = []
        
        try:
            with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
                # Security check for dangerous paths
                for member in zip_ref.namelist():
                    self.validator.validate_archive_path(member)
                
                for member in zip_ref.namelist():
                    # Skip directories
                    if member.endswith('/'):
                        continue
                    
                    try:
                        member_content = zip_ref.read(member)
                        full_path = f"{base_path}/{member}" if base_path else member
                        
                        # Check if this file is also an archive
                        is_nested_archive, archive_type = self.validator.is_archive_file(member)
                        
                        if is_nested_archive and member_content:
                            try:
                                nested_files = self.extract_archive(
                                    member_content, 
                                    member, 
                                    base_path=self._get_base_path_for_archive(full_path, archive_type),
                                    base_uuid=base_uuid, 
                                    current_depth=current_depth + 1
                                )
                                extracted_files.extend(nested_files)
                            except (tarfile.TarError, zipfile.BadZipFile, OSError, gzip.BadGzipFile):
                                # If it's not actually a valid archive, treat as regular file
                                extracted_files.append((member_content, member, full_path))
                        else:
                            # Regular file
                            extracted_files.append((member_content, member, full_path))
                    
                    except Exception as e:
                        # Skip corrupted files but continue with others
                        continue
                        
        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Invalid ZIP file")
        
        return extracted_files
    
    def _extract_tar(self, tar_content: bytes, base_path: str, base_uuid: str, 
                    current_depth: int) -> List[Tuple[bytes, str, str]]:
        """Extract TAR archive recursively"""
        extracted_files = []
        
        try:
            with tarfile.open(fileobj=io.BytesIO(tar_content), mode='r:*') as tar_ref:
                # Security check for dangerous paths
                for member in tar_ref.getnames():
                    self.validator.validate_archive_path(member)
                
                for member in tar_ref.getmembers():
                    # Skip directories
                    if member.isdir():
                        continue
                    
                    try:
                        file_obj = tar_ref.extractfile(member)
                        if file_obj is None:
                            continue
                        
                        member_content = file_obj.read()
                        full_path = f"{base_path}/{member.name}" if base_path else member.name
                        
                        # Check if this file is also an archive
                        is_nested_archive, archive_type = self.validator.is_archive_file(member.name)
                        
                        if is_nested_archive and member_content:
                            try:
                                nested_files = self.extract_archive(
                                    member_content, 
                                    member.name, 
                                    base_path=self._get_base_path_for_archive(full_path, archive_type),
                                    base_uuid=base_uuid, 
                                    current_depth=current_depth + 1
                                )
                                extracted_files.extend(nested_files)
                            except (tarfile.TarError, zipfile.BadZipFile, OSError, gzip.BadGzipFile):
                                # If it's not actually a valid archive, treat as regular file
                                extracted_files.append((member_content, member.name, full_path))
                        else:
                            # Regular file
                            extracted_files.append((member_content, member.name, full_path))
                    
                    except Exception as e:
                        # Skip corrupted files but continue with others
                        continue
                        
        except tarfile.TarError:
            raise HTTPException(status_code=400, detail="Invalid TAR file")
        
        return extracted_files
    
    def _extract_gz(self, gz_content: bytes, base_path: str, base_uuid: str, 
                   current_depth: int) -> List[Tuple[bytes, str, str]]:
        """Extract GZ file (single file compression)"""
        try:
            # Decompress the GZ file
            decompressed_content = gzip.decompress(gz_content)
            
            # Determine decompressed filename
            if base_path.endswith('.gz'):
                decompressed_filename = base_path[:-3]  # Remove .gz extension
            else:
                decompressed_filename = base_path + '_decompressed'
            
            # Check if decompressed content is an archive
            is_nested_archive, archive_type = self.validator.is_archive_file(decompressed_filename)
            
            if is_nested_archive and decompressed_content:
                try:
                    return self.extract_archive(
                        decompressed_content, 
                        decompressed_filename, 
                        base_path=self._get_base_path_for_archive(decompressed_filename, archive_type),
                        base_uuid=base_uuid, 
                        current_depth=current_depth + 1
                    )
                except (tarfile.TarError, zipfile.BadZipFile, OSError, gzip.BadGzipFile):
                    # If it's not actually a valid archive, treat as regular file
                    pass
            
            # Return as regular file
            import os
            original_filename = os.path.basename(decompressed_filename)
            return [(decompressed_content, original_filename, decompressed_filename)]
            
        except (OSError, gzip.BadGzipFile):
            raise HTTPException(status_code=400, detail="Invalid GZ file")
    
    def _get_base_path_for_archive(self, full_path: str, archive_type: str) -> str:
        """Get base path for nested archive extraction"""
        if archive_type == 'tar.gz':
            # Remove .tar.gz extension
            return full_path.rsplit('.', 2)[0] if full_path.count('.') >= 2 else full_path.rsplit('.', 1)[0]
        else:
            # Remove single extension
            return full_path.rsplit('.', 1)[0]