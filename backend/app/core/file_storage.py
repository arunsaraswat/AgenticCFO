"""File storage service for handling file uploads and artifact storage."""
import hashlib
import os
import shutil
import uuid
from pathlib import Path
from typing import BinaryIO, Optional

from fastapi import UploadFile


class FileStorageService:
    """
    Service for storing and retrieving files from local filesystem.

    For MVP, files are stored locally. In production, this can be swapped
    for S3/CloudFront without changing the interface.

    Attributes:
        upload_dir: Base directory for uploaded files
        artifacts_dir: Base directory for generated artifacts
    """

    def __init__(self, upload_dir: str, artifacts_dir: str):
        """
        Initialize file storage service.

        Args:
            upload_dir: Path to upload directory
            artifacts_dir: Path to artifacts directory
        """
        self.upload_dir = Path(upload_dir)
        self.artifacts_dir = Path(artifacts_dir)

        # Create directories if they don't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def calculate_file_hash(self, file: BinaryIO) -> str:
        """
        Calculate SHA-256 hash of file contents.

        Args:
            file: Binary file object

        Returns:
            64-character hex string (SHA-256 hash)
        """
        sha256_hash = hashlib.sha256()
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        # Reset file pointer to beginning
        file.seek(0)
        return sha256_hash.hexdigest()

    async def save_upload(
        self, file: UploadFile, tenant_id: int, file_hash: Optional[str] = None
    ) -> tuple[str, str, int]:
        """
        Save uploaded file to storage with path traversal protection.

        Files are organized by tenant: uploads/{tenant_id}/{hash}/{safe_filename}

        Args:
            file: FastAPI UploadFile object
            tenant_id: Tenant ID for organizing files
            file_hash: Pre-calculated file hash (optional)

        Returns:
            Tuple of (file_path, file_hash, file_size_bytes)

        Raises:
            ValueError: If filename contains path traversal attempts
        """
        # Calculate hash if not provided
        if file_hash is None:
            file_hash = self.calculate_file_hash(file.file)

        # Sanitize filename to prevent path traversal attacks
        # Extract basename only (removes any path components like ../)
        original_filename = Path(file.filename).name

        # Generate safe filename: uuid_originalname to prevent collisions
        safe_filename = f"{uuid.uuid4().hex}_{original_filename}"

        # Create tenant directory
        tenant_dir = self.upload_dir / str(tenant_id) / file_hash
        tenant_dir.mkdir(parents=True, exist_ok=True)

        # Construct file path with sanitized filename
        file_path = tenant_dir / safe_filename

        # Defense in depth: Ensure resolved path is within upload_dir
        # This prevents path traversal even if sanitization is bypassed
        try:
            if not file_path.resolve().is_relative_to(self.upload_dir.resolve()):
                raise ValueError("Invalid file path detected (path traversal attempt)")
        except (ValueError, AttributeError):
            # is_relative_to not available in Python <3.9, fallback check
            if not str(file_path.resolve()).startswith(str(self.upload_dir.resolve())):
                raise ValueError("Invalid file path detected (path traversal attempt)")

        # Save file with sanitized path
        file_size = 0

        with open(file_path, "wb") as buffer:
            # Read and write in chunks
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(chunk)
                file_size += len(chunk)

        return str(file_path), file_hash, file_size

    def save_artifact(
        self, content: bytes, tenant_id: int, work_order_id: int, filename: str
    ) -> tuple[str, str, int]:
        """
        Save generated artifact to storage with path traversal protection.

        Artifacts are organized by tenant and work order:
        artifacts/{tenant_id}/{work_order_id}/{safe_filename}

        Args:
            content: File content as bytes
            tenant_id: Tenant ID
            work_order_id: Work order ID
            filename: Artifact filename

        Returns:
            Tuple of (file_path, file_hash, file_size_bytes)

        Raises:
            ValueError: If filename contains path traversal attempts
        """
        # Calculate hash
        file_hash = hashlib.sha256(content).hexdigest()

        # Sanitize filename to prevent path traversal attacks
        safe_filename = Path(filename).name

        # Create work order directory
        work_order_dir = self.artifacts_dir / str(tenant_id) / str(work_order_id)
        work_order_dir.mkdir(parents=True, exist_ok=True)

        # Construct file path with sanitized filename
        file_path = work_order_dir / safe_filename

        # Defense in depth: Ensure resolved path is within artifacts_dir
        try:
            if not file_path.resolve().is_relative_to(self.artifacts_dir.resolve()):
                raise ValueError("Invalid file path detected (path traversal attempt)")
        except (ValueError, AttributeError):
            # is_relative_to not available in Python <3.9, fallback check
            if not str(file_path.resolve()).startswith(str(self.artifacts_dir.resolve())):
                raise ValueError("Invalid file path detected (path traversal attempt)")

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        file_size = len(content)

        return str(file_path), file_hash, file_size

    def get_file_path(self, file_path: str) -> Path:
        """
        Get Path object for file.

        Args:
            file_path: String file path

        Returns:
            Path object
        """
        return Path(file_path)

    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists.

        Args:
            file_path: String file path

        Returns:
            True if file exists, False otherwise
        """
        return Path(file_path).exists()

    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage.

        Args:
            file_path: String file path

        Returns:
            True if deleted successfully, False if file didn't exist
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False

    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.

        Args:
            file_path: String file path

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        return Path(file_path).stat().st_size


# Singleton instance
_storage_service: Optional[FileStorageService] = None


def get_file_storage_service() -> FileStorageService:
    """
    Get file storage service singleton instance.

    Returns:
        FileStorageService instance
    """
    global _storage_service
    if _storage_service is None:
        # Import here to avoid circular dependency
        from app.core.config import settings

        _storage_service = FileStorageService(
            upload_dir=settings.upload_dir, artifacts_dir=settings.artifacts_dir
        )
    return _storage_service
