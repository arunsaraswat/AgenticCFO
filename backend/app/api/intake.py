"""File intake API endpoints for uploading and processing files."""
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_current_user, get_db
from app.core.exceptions import (
    ColumnMappingError,
    DataQualityError,
    FileParseError,
    FileSizeExceededError,
    InvalidFileTypeError,
    TemplateDetectionError,
)
from app.core.file_storage import get_file_storage_service
from app.models.user import User
from app.schemas.dataset import DatasetResponse
from app.schemas.file_upload import FileUploadResponse, FileUploadUpdate
from app.services.audit_service import AuditService
from app.services.dataset_service import DatasetService
from app.services.file_service import FileUploadService

router = APIRouter(prefix="/intake", tags=["File Intake"])


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    request: Request,
    file: UploadFile = File(..., description="File to upload (Excel or CSV)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileUploadResponse:
    """
    Upload a file for processing.

    Accepts Excel (.xlsx, .xls) or CSV files up to configured max size.
    Files are:
    1. Validated for size and type
    2. Saved to storage with SHA-256 hash
    3. Deduplicated (returns existing record if hash matches)
    4. Recorded in database with status='processing'

    Args:
        file: Uploaded file
        current_user: Authenticated user
        db: Database session

    Returns:
        FileUploadResponse with upload details

    Raises:
        HTTPException 400: If file is invalid (size, type, etc.)
        HTTPException 413: If file exceeds max size
    """
    # Validate file exists
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    # Validate file size BEFORE processing (prevents DoS attacks)
    content_length = request.headers.get("content-length")
    if content_length:
        size_bytes = int(content_length)
        max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

        if size_bytes > max_size_bytes:
            size_mb = size_bytes / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size ({size_mb:.2f}MB) exceeds maximum ({settings.max_upload_size_mb}MB)",
            )

    # Validate file extension
    allowed_extensions = {".xlsx", ".xls", ".csv"}
    file_ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}",
        )

    file_upload = None
    file_path_for_cleanup = None

    # Extract client info for audit logging
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    try:
        # Step 1: Save file to storage (outside transaction)
        file_upload = await FileUploadService.process_upload(
            db=db, file=file, tenant_id=current_user.tenant_id, user_id=current_user.id
        )
        file_path_for_cleanup = file_upload.file_path

        # Audit Log: File uploaded
        AuditService.log_file_upload(
            db=db,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            file_upload_id=file_upload.id,
            filename=file_upload.filename,
            file_size_bytes=file_upload.file_size_bytes,
            file_hash=file_upload.file_hash,
            ip_address=client_ip,
            user_agent=user_agent,
        )

        # Step 2: Process file in database transaction
        # This ensures atomicity: either all database changes succeed or all are rolled back
        try:
            # Trigger dataset processing (template detection + column mapping + DQ validation)
            dataset, processing_results = await DatasetService.process_file_upload(
                db=db,
                tenant_id=current_user.tenant_id,
                file_upload_id=file_upload.id,
                file_path=file_upload.file_path,
            )

            # Update file upload status based on processing results
            if dataset:
                FileUploadService.update_file_upload(
                    db=db,
                    file_upload_id=file_upload.id,
                    tenant_id=current_user.tenant_id,
                    update_data=FileUploadUpdate(status="completed"),
                )

                # Audit Log: Dataset created successfully
                AuditService.log_dataset_created(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    dataset_id=dataset.id,
                    template_type=dataset.template_type,
                    template_confidence=dataset.dataset_metadata.get("template_confidence", 0.0),
                    mapping_confidence=dataset.dataset_metadata.get("mapping_confidence", 0.0),
                    dq_status=dataset.dq_status,
                )

                # Audit Log: DQ validation results
                if dataset.dq_results:
                    AuditService.log_dq_validation(
                        db=db,
                        tenant_id=current_user.tenant_id,
                        dataset_id=dataset.id,
                        dq_status=dataset.dq_results.get("status", "unknown"),
                        error_count=dataset.dq_results.get("error_count", 0),
                        warning_count=dataset.dq_results.get("warning_count", 0),
                        checks=dataset.dq_results.get("checks", {}),
                    )

                # Commit transaction on success
                db.commit()
            else:
                # Processing failed - rollback transaction
                db.rollback()
                error_message = "; ".join(processing_results.get("errors", ["Unknown error"]))

                # Audit Log: Processing failed
                AuditService.log_dataset_processing_failed(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_upload_id=file_upload.id,
                    error_message=error_message,
                    processing_results=processing_results,
                )

                # Create new transaction for status update
                FileUploadService.update_file_upload(
                    db=db,
                    file_upload_id=file_upload.id,
                    tenant_id=current_user.tenant_id,
                    update_data=FileUploadUpdate(status="failed", error_message=error_message),
                )
                db.commit()

        except Exception as processing_error:
            # Rollback transaction on any processing error
            db.rollback()

            # Try to update status to failed (in new transaction)
            try:
                FileUploadService.update_file_upload(
                    db=db,
                    file_upload_id=file_upload.id,
                    tenant_id=current_user.tenant_id,
                    update_data=FileUploadUpdate(
                        status="failed",
                        error_message=f"Processing error: {str(processing_error)}"
                    ),
                )
                db.commit()
            except Exception:
                pass  # Status update failed, but we'll still raise the original error

            # Clean up uploaded file if processing failed
            storage = get_file_storage_service()
            storage.delete_file(file_path_for_cleanup)

            # Audit Log: File deleted due to processing failure
            try:
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Processing failed: {str(processing_error)}"
                )
                db.commit()
            except Exception:
                pass  # Audit logging failed, but continue with raising original error

            raise processing_error

        # Refresh to get latest status
        db.refresh(file_upload)
        return FileUploadResponse.model_validate(file_upload)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise

    # Handle file parsing errors (422 Unprocessable Entity)
    except FileParseError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Parse error: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"File parsing failed: {str(e)}. Please check file format and structure.",
        )

    # Handle template detection errors (422 Unprocessable Entity)
    except TemplateDetectionError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Template detection failed: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Template detection failed: {str(e)}. File structure does not match any known template.",
        )

    # Handle column mapping errors (422 Unprocessable Entity)
    except ColumnMappingError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Column mapping failed: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Column mapping failed: {str(e)}. Unable to match file columns to template schema.",
        )

    # Handle data quality errors (422 Unprocessable Entity)
    except DataQualityError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Data quality validation failed: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Data quality validation failed: {str(e)}",
        )

    # Handle invalid file type (400 Bad Request)
    except InvalidFileTypeError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Invalid file type: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # Handle file size exceeded (413 Request Entity Too Large)
    except FileSizeExceededError as e:
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"File size exceeded: {str(e)}"
                )
                db.commit()
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )

    # Generic catch-all for unexpected errors (500 Internal Server Error)
    except Exception as e:
        # Clean up file if initial upload succeeded but later steps failed
        if file_path_for_cleanup:
            try:
                storage = get_file_storage_service()
                storage.delete_file(file_path_for_cleanup)

                # Audit Log: File deleted due to upload failure
                AuditService.log_file_deleted(
                    db=db,
                    tenant_id=current_user.tenant_id,
                    user_id=current_user.id,
                    file_path=file_path_for_cleanup,
                    reason=f"Unexpected error: {str(e)}"
                )
                db.commit()
            except Exception:
                pass  # Cleanup or audit logging failed, but log the original error

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed due to an unexpected error. Please contact support.",
        )


@router.get("/uploads", response_model=List[FileUploadResponse])
def list_uploads(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[FileUploadResponse]:
    """
    List all file uploads for the current user's tenant.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of FileUploadResponse objects
    """
    file_uploads = FileUploadService.list_file_uploads(
        db=db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
    return [FileUploadResponse.model_validate(upload) for upload in file_uploads]


@router.get("/uploads/{file_upload_id}", response_model=FileUploadResponse)
def get_upload(
    file_upload_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileUploadResponse:
    """
    Get details of a specific file upload.

    Args:
        file_upload_id: File upload ID
        current_user: Authenticated user
        db: Database session

    Returns:
        FileUploadResponse with upload details

    Raises:
        HTTPException 404: If upload not found
    """
    file_upload = FileUploadService.get_file_upload(
        db=db, file_upload_id=file_upload_id, tenant_id=current_user.tenant_id
    )

    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File upload not found"
        )

    return FileUploadResponse.model_validate(file_upload)


@router.get("/datasets", response_model=List[DatasetResponse])
def list_datasets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DatasetResponse]:
    """
    List all datasets for the current user's tenant.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of DatasetResponse objects with template detection and mapping results
    """
    datasets = DatasetService.list_datasets(
        db=db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
    return [DatasetResponse.model_validate(dataset) for dataset in datasets]


@router.get("/datasets/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DatasetResponse:
    """
    Get details of a specific dataset including DQ validation results.

    Args:
        dataset_id: Dataset ID
        current_user: Authenticated user
        db: Database session

    Returns:
        DatasetResponse with full processing details

    Raises:
        HTTPException 404: If dataset not found
    """
    dataset = DatasetService.get_dataset(
        db=db, dataset_id=dataset_id, tenant_id=current_user.tenant_id
    )

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found"
        )

    return DatasetResponse.model_validate(dataset)
