import mimetypes
from typing import Tuple, List

from fastapi import HTTPException


class FileValidator:
    """
    Service for file validation and security checks
    """
    
    def __init__(self):
        self.max_file_size = 1024 * 1024 * 1024  # 1GB
        self.max_archive_size = 1024 * 1024 * 1024  # 1GB
        
        self.allowed_extensions = {
            # Documents
            '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.odt', '.ods', '.odp', '.rtf',
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp',
            # Audio
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
            # Video
            '.mp4', '.avi', '.mov', '.wmv', '.webm', '.mkv', '.flv', '.m4v',
            '.3gp', '.mpg', '.mpeg', '.ogv', '.ts', '.mts', '.vob',
            # Archives
            '.zip', '.tar', '.gz', '.tgz', '.tar.gz',
            # Data files
            '.csv', '.json', '.xml', '.yaml', '.yml',
            # Code files
            '.py', '.js', '.html', '.css', '.sql', '.md',
        }
        
        self.previewable_types = [
            'text/',           # Text files
            'image/',          # Images
            'application/pdf', # PDF files
            'application/json',# JSON files
            'application/xml', # XML files
            'video/',          # Video files
            'audio/',          # Audio files
        ]
    
    def validate_file_upload(self, filename: str, content: bytes, content_type: str = None) -> None:
        """
        Validate file for upload
        
        Args:
            filename (str): Original filename
            content (bytes): File content
            content_type (str): MIME type
            
        Raises:
            HTTPException: If validation fails
        """
        # Check filename
        if not filename or filename.strip() == '':
            raise HTTPException(status_code=400, detail="Filename cannot be empty")
        
        # Check file size
        file_size = len(content)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File cannot be empty")
        
        is_archive, _ = self.is_archive_file(filename, content_type)
        max_size = self.max_archive_size if is_archive else self.max_file_size
        
        if file_size > max_size:
            size_mb = max_size / (1024 * 1024)
            file_type = "archive" if is_archive else "file"
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum {file_type} size is {size_mb}MB"
            )
        
        # Check file extension
        self.validate_file_extension(filename)
        
        # Security checks
        self.validate_filename_security(filename)
    
    def validate_file_extension(self, filename: str) -> None:
        """
        Validate file extension
        
        Args:
            filename (str): Filename to validate
            
        Raises:
            HTTPException: If extension is not allowed
        """
        filename_lower = filename.lower()
        
        # Check for allowed extensions
        is_allowed = any(filename_lower.endswith(ext) for ext in self.allowed_extensions)
        
        if not is_allowed:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Allowed extensions: {', '.join(sorted(self.allowed_extensions))}"
            )
    
    def validate_filename_security(self, filename: str) -> None:
        """
        Validate filename for security issues
        
        Args:
            filename (str): Filename to validate
            
        Raises:
            HTTPException: If security validation fails
        """
        # Check for dangerous characters
        dangerous_chars = ['<', '>', '"', '|', '?', '*', ':', '\\']
        if any(char in filename for char in dangerous_chars):
            raise HTTPException(status_code=400, detail="Filename contains illegal characters")
        
        # Check for path traversal
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            raise HTTPException(status_code=400, detail="Invalid filename path")
        
        # Check filename length
        if len(filename) > 255:
            raise HTTPException(status_code=400, detail="Filename too long (max 255 characters)")
    
    def validate_archive_path(self, path: str) -> None:
        """
        Validate path from archive extraction
        
        Args:
            path (str): Path to validate
            
        Raises:
            HTTPException: If path is dangerous
        """
        if path.startswith('/') or '..' in path:
            raise HTTPException(status_code=400, detail="Invalid file path in archive")
    
    def is_archive_file(self, filename: str, content_type: str = None) -> Tuple[bool, str]:
        """
        Check if file is an archive and return archive type
        
        Args:
            filename (str): Filename to check
            content_type (str): MIME type
            
        Returns:
            Tuple[bool, str]: (is_archive, archive_type)
        """
        filename_lower = filename.lower()
        
        # ZIP files
        if filename_lower.endswith('.zip') or content_type == 'application/zip':
            return True, 'zip'
        
        # TAR files
        if (filename_lower.endswith('.tar') or 
            content_type in ['application/x-tar', 'application/tar']):
            return True, 'tar'
        
        # TAR.GZ files
        if (filename_lower.endswith('.tar.gz') or filename_lower.endswith('.tgz') or
            content_type in ['application/gzip', 'application/x-gzip', 'application/x-tar-gz']):
            return True, 'tar.gz'
        
        # GZ files (single file compression)
        if (filename_lower.endswith('.gz') and not filename_lower.endswith('.tar.gz') or
            content_type in ['application/gzip', 'application/x-gzip']):
            return True, 'gz'
        
        return False, None
    
    def is_previewable(self, content_type: str) -> bool:
        """
        Check if file type is previewable
        
        Args:
            content_type (str): MIME type
            
        Returns:
            bool: True if previewable
        """
        return any(content_type.startswith(ptype) or content_type == ptype 
                  for ptype in self.previewable_types)
    
    def get_content_type(self, filename: str) -> str:
        """
        Get content type for filename
        
        Args:
            filename (str): Filename
            
        Returns:
            str: MIME type
        """
        content_type, _ = mimetypes.guess_type(filename)
        return content_type if content_type else 'application/octet-stream'