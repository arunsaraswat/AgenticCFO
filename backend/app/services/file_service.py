"""Service layer for file upload operations."""
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.file_storage import get_file_storage_service
from app.models.file_upload import FileUpload
from app.schemas.file_upload import FileUploadCreate, FileUploadUpdate


class FileUploadService:
    """
    Service for managing file uploads.

    Handles file storage, database records, and validation.
    """

    @staticmethod
    def create_file_upload(
        db: Session, tenant_id: int, file_upload_data: FileUploadCreate
    ) -> FileUpload:
        """
        Create a new file upload record.

        Args:
            db: Database session
            tenant_id: Tenant ID
            file_upload_data: File upload creation data

        Returns:
            Created FileUpload instance
        """
        file_upload = FileUpload(
            tenant_id=tenant_id,
            filename=file_upload_data.filename,
            file_path=file_upload_data.file_path,
            file_hash=file_upload_data.file_hash,
            file_size_bytes=file_upload_data.file_size_bytes,
            mime_type=file_upload_data.mime_type,
            upload_channel=file_upload_data.upload_channel,
            uploaded_by_user_id=file_upload_data.uploaded_by_user_id,
            status="processing",  # Initial status
            created_at=datetime.utcnow(),
        )
        db.add(file_upload)
        db.commit()
        db.refresh(file_upload)
        return file_upload

    @staticmethod
    def get_file_upload(db: Session, file_upload_id: int, tenant_id: int) -> Optional[FileUpload]:
        """
        Get file upload by ID.

        Args:
            db: Database session
            file_upload_id: File upload ID
            tenant_id: Tenant ID for filtering

        Returns:
            FileUpload instance or None if not found
        """
        return (
            db.query(FileUpload)
            .filter(FileUpload.id == file_upload_id, FileUpload.tenant_id == tenant_id)
            .first()
        )

    @staticmethod
    def get_file_upload_by_hash(db: Session, file_hash: str, tenant_id: int) -> Optional[FileUpload]:
        """
        Get file upload by hash (for deduplication).

        Args:
            db: Database session
            file_hash: SHA-256 file hash
            tenant_id: Tenant ID for filtering

        Returns:
            FileUpload instance or None if not found
        """
        return (
            db.query(FileUpload)
            .filter(FileUpload.file_hash == file_hash, FileUpload.tenant_id == tenant_id)
            .first()
        )

    @staticmethod
    def update_file_upload(
        db: Session, file_upload_id: int, tenant_id: int, update_data: FileUploadUpdate
    ) -> Optional[FileUpload]:
        """
        Update file upload record.

        Args:
            db: Database session
            file_upload_id: File upload ID
            tenant_id: Tenant ID for filtering
            update_data: Update data

        Returns:
            Updated FileUpload instance or None if not found
        """
        file_upload = FileUploadService.get_file_upload(db, file_upload_id, tenant_id)
        if not file_upload:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(file_upload, key, value)

        db.commit()
        db.refresh(file_upload)
        return file_upload

    @staticmethod
    def list_file_uploads(
        db: Session, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> list[FileUpload]:
        """
        List file uploads for a tenant.

        Args:
            db: Database session
            tenant_id: Tenant ID for filtering
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of FileUpload instances
        """
        return (
            db.query(FileUpload)
            .filter(FileUpload.tenant_id == tenant_id)
            .order_by(FileUpload.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    async def process_upload(
        db: Session, file: UploadFile, tenant_id: int, user_id: Optional[int] = None
    ) -> FileUpload:
        """
        Process file upload: save to storage and create DB record.

        Args:
            db: Database session
            file: FastAPI UploadFile object
            tenant_id: Tenant ID
            user_id: Uploading user ID (optional)

        Returns:
            Created FileUpload instance
        """
        storage = get_file_storage_service()

        # Calculate hash and save file
        file_hash = storage.calculate_file_hash(file.file)

        # Check for duplicate (deduplication)
        existing = FileUploadService.get_file_upload_by_hash(db, file_hash, tenant_id)
        if existing:
            # File already exists, return existing record
            return existing

        # Save file to storage
        file_path, file_hash, file_size = await storage.save_upload(file, tenant_id, file_hash)

        # Create database record
        file_upload_data = FileUploadCreate(
            filename=file.filename,
            file_path=file_path,
            file_hash=file_hash,
            file_size_bytes=file_size,
            mime_type=file.content_type,
            upload_channel="web",
            uploaded_by_user_id=user_id,
        )

        return FileUploadService.create_file_upload(db, tenant_id, file_upload_data)
