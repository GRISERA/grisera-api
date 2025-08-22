import os
from datetime import timedelta
from typing import Optional, Dict, Any

from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException


class MinIOClient:
    """
    MinIO client wrapper for file storage operations
    """
    
    def __init__(self, bucket_name: str):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.endpoint = os.getenv("MINIO_ENDPOINT", "s3:9000")
        self.public_endpoint_url = os.getenv("MINIO_PUBLIC_ENDPOINT", "http://localhost:9000")
        self.bucket_name = bucket_name
        
        # Parse public endpoint URL
        from urllib.parse import urlparse
        parsed = urlparse(self.public_endpoint_url)
        self.public_endpoint = parsed.netloc  # This includes port if specified
        
        self._client = None
        self._public_client = None
    
    def _is_secure_endpoint(self, url: str) -> bool:
        """Check if endpoint should use secure connection"""
        return url.startswith('https://')
    
    @property
    def client(self) -> Minio:
        """Get MinIO client instance"""
        if self._client is None:
            self._client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=False,  # Internal endpoint is typically http
                region=self.region,
            )
        return self._client
    
    @property
    def public_client(self) -> Minio:
        """Get public MinIO client instance for URL generation"""
        if self._public_client is None:
            secure = self._is_secure_endpoint(self.public_endpoint_url)
            self._public_client = Minio(
                self.public_endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=secure,
                region=self.region,
            )
        return self._public_client
    
    def ensure_bucket_exists(self) -> None:
        """Ensure the bucket exists, create if it doesn't"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                # Set bucket to private by default (no public policy)
                self._ensure_bucket_is_private()
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to create bucket: {str(e)}")
    
    def _ensure_bucket_is_private(self) -> None:
        """Ensure bucket has no public read policy"""
        try:
            # Remove any existing bucket policy to make it private
            self.client.delete_bucket_policy(self.bucket_name)
        except S3Error:
            # Ignore errors - bucket might not have any policy set
            pass
    
    def make_bucket_private(self) -> None:
        """
        Explicitly make bucket private (can be called manually for existing buckets)
        """
        try:
            self._ensure_bucket_is_private()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to make bucket private: {str(e)}")
    
    def upload_file(self, object_name: str, file_data: bytes, content_type: str) -> None:
        """
        Upload file to MinIO storage
        
        Args:
            object_name (str): Object name in storage
            file_data (bytes): File content
            content_type (str): MIME type
        """
        try:
            import io
            
            self.ensure_bucket_exists()
            
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                self.bucket_name,
                object_name,
                file_stream,
                length=len(file_data),
                content_type=content_type,
            )
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    
    def get_file(self, object_name: str):
        """
        Get file from MinIO storage
        
        Args:
            object_name (str): Object name in storage
            
        Returns:
            MinIO response object
        """
        try:
            return self.client.get_object(self.bucket_name, object_name)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to get file: {str(e)}")
    
    def delete_file(self, object_name: str) -> None:
        """
        Delete file from MinIO storage
        
        Args:
            object_name (str): Object name in storage
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
    
    def generate_download_url(self, object_name: str, original_filename: str, 
                            expires_hours: int = 1) -> Dict[str, Any]:
        """
        Generate pre-signed download URL
        
        Args:
            object_name (str): Object name in storage
            original_filename (str): Original filename for download
            expires_hours (int): URL expiration time in hours
            
        Returns:
            Dict with download URL and metadata
        """
        try:
            download_url = self.public_client.presigned_get_object(
                self.bucket_name, 
                object_name,
                expires=timedelta(hours=expires_hours),
                response_headers={
                    'response-content-disposition': f'attachment; filename="{original_filename}"'
                }
            )
            
            return {
                "download_url": download_url,
                "filename": original_filename,
                "expires_in": expires_hours * 3600
            }
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")
    
    def generate_preview_url(self, object_name: str, content_type: str = None,
                           expires_hours: int = 1) -> Dict[str, Any]:
        """
        Generate pre-signed preview URL for viewing file in browser
        
        Args:
            object_name (str): Object name in storage
            content_type (str): MIME type for proper browser rendering
            expires_hours (int): URL expiration time in hours
            
        Returns:
            Dict with preview URL and metadata
        """
        try:
            # Response headers for inline viewing (no download)
            response_headers = {}
            if content_type:
                response_headers['response-content-type'] = content_type
            
            preview_url = self.public_client.presigned_get_object(
                self.bucket_name, 
                object_name,
                expires=timedelta(hours=expires_hours),
                response_headers=response_headers if response_headers else None
            )
            
            return {
                "preview_url": preview_url,
                "expires_in": expires_hours * 3600
            }
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate preview URL: {str(e)}")