"""Service layer for audit event logging.

Per CLAUDE.md requirements: "Control logging: 100% actions logged"
All significant events must be logged to the audit_events table for compliance.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


class AuditService:
    """
    Service for logging audit events.

    Creates immutable audit trail entries for all significant system events.
    Audit events are never updated or deleted (append-only log).
    """

    @staticmethod
    def log_event(
        db: Session,
        tenant_id: int,
        event_type: str,
        event_category: str,
        details: dict,
        user_id: Optional[int] = None,
        work_order_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEvent:
        """
        Log an audit event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            event_type: Type of event (e.g., "file.uploaded", "dataset.created")
            event_category: Category (intake, orchestration, agent, control, output, auth)
            details: Event-specific details as dict
            user_id: User who triggered the event (optional)
            work_order_id: Related work order (optional)
            ip_address: IP address of request (optional)
            user_agent: User agent string (optional)

        Returns:
            Created AuditEvent instance
        """
        audit_event = AuditEvent(
            tenant_id=tenant_id,
            work_order_id=work_order_id,
            event_type=event_type,
            event_category=event_category,
            user_id=user_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow(),
        )

        db.add(audit_event)
        db.commit()
        db.refresh(audit_event)

        return audit_event

    @staticmethod
    def log_file_upload(
        db: Session,
        tenant_id: int,
        user_id: int,
        file_upload_id: int,
        filename: str,
        file_size_bytes: int,
        file_hash: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEvent:
        """
        Log file upload event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            user_id: User who uploaded the file
            file_upload_id: File upload ID
            filename: Original filename
            file_size_bytes: File size in bytes
            file_hash: SHA-256 file hash
            ip_address: IP address (optional)
            user_agent: User agent (optional)

        Returns:
            Created AuditEvent instance
        """
        return AuditService.log_event(
            db=db,
            tenant_id=tenant_id,
            event_type="file.uploaded",
            event_category="intake",
            user_id=user_id,
            details={
                "file_upload_id": file_upload_id,
                "filename": filename,
                "file_size_bytes": file_size_bytes,
                "file_hash": file_hash,
            },
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def log_dataset_created(
        db: Session,
        tenant_id: int,
        user_id: int,
        dataset_id: int,
        template_type: str,
        template_confidence: float,
        mapping_confidence: float,
        dq_status: str,
    ) -> AuditEvent:
        """
        Log dataset creation event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            user_id: User who triggered creation
            dataset_id: Dataset ID
            template_type: Detected template type
            template_confidence: Template detection confidence
            mapping_confidence: Column mapping confidence
            dq_status: Data quality status

        Returns:
            Created AuditEvent instance
        """
        return AuditService.log_event(
            db=db,
            tenant_id=tenant_id,
            event_type="dataset.created",
            event_category="intake",
            user_id=user_id,
            details={
                "dataset_id": dataset_id,
                "template_type": template_type,
                "template_confidence": template_confidence,
                "mapping_confidence": mapping_confidence,
                "dq_status": dq_status,
            },
        )

    @staticmethod
    def log_dataset_processing_failed(
        db: Session,
        tenant_id: int,
        user_id: int,
        file_upload_id: int,
        error_message: str,
        processing_results: dict,
    ) -> AuditEvent:
        """
        Log dataset processing failure event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            user_id: User who triggered processing
            file_upload_id: File upload ID
            error_message: Error message
            processing_results: Processing results dict

        Returns:
            Created AuditEvent instance
        """
        return AuditService.log_event(
            db=db,
            tenant_id=tenant_id,
            event_type="dataset.processing_failed",
            event_category="intake",
            user_id=user_id,
            details={
                "file_upload_id": file_upload_id,
                "error_message": error_message,
                "processing_results": processing_results,
            },
        )

    @staticmethod
    def log_dq_validation(
        db: Session,
        tenant_id: int,
        dataset_id: int,
        dq_status: str,
        error_count: int,
        warning_count: int,
        checks: dict,
    ) -> AuditEvent:
        """
        Log data quality validation event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            dataset_id: Dataset ID
            dq_status: Validation status (passed, warning, failed)
            error_count: Number of failed checks
            warning_count: Number of warning checks
            checks: Detailed check results

        Returns:
            Created AuditEvent instance
        """
        return AuditService.log_event(
            db=db,
            tenant_id=tenant_id,
            event_type="dq.validation_completed",
            event_category="control",
            details={
                "dataset_id": dataset_id,
                "dq_status": dq_status,
                "error_count": error_count,
                "warning_count": warning_count,
                "checks": checks,
            },
        )

    @staticmethod
    def log_file_deleted(
        db: Session,
        tenant_id: int,
        user_id: Optional[int],
        file_path: str,
        reason: str,
    ) -> AuditEvent:
        """
        Log file deletion event.

        Args:
            db: Database session
            tenant_id: Tenant ID
            user_id: User who deleted the file (optional for system deletions)
            file_path: Path to deleted file
            reason: Reason for deletion

        Returns:
            Created AuditEvent instance
        """
        return AuditService.log_event(
            db=db,
            tenant_id=tenant_id,
            event_type="file.deleted",
            event_category="intake",
            user_id=user_id,
            details={
                "file_path": file_path,
                "reason": reason,
            },
        )

    @staticmethod
    def get_audit_trail(
        db: Session,
        tenant_id: int,
        event_type: Optional[str] = None,
        event_category: Optional[str] = None,
        user_id: Optional[int] = None,
        work_order_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditEvent]:
        """
        Query audit trail with filters.

        Args:
            db: Database session
            tenant_id: Tenant ID
            event_type: Filter by event type (optional)
            event_category: Filter by category (optional)
            user_id: Filter by user (optional)
            work_order_id: Filter by work order (optional)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of AuditEvent instances
        """
        query = db.query(AuditEvent).filter(AuditEvent.tenant_id == tenant_id)

        if event_type:
            query = query.filter(AuditEvent.event_type == event_type)

        if event_category:
            query = query.filter(AuditEvent.event_category == event_category)

        if user_id:
            query = query.filter(AuditEvent.user_id == user_id)

        if work_order_id:
            query = query.filter(AuditEvent.work_order_id == work_order_id)

        return (
            query.order_by(AuditEvent.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
