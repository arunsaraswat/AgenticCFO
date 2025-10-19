"""Artifact API endpoints for downloading generated files."""
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.artifact import Artifact
from app.models.user import User
from app.models.work_order import WorkOrder
from app.schemas.artifact import ArtifactResponse

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])


@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(
    artifact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ArtifactResponse:
    """
    Get artifact metadata by ID.

    Args:
        artifact_id: Artifact ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Artifact metadata

    Raises:
        HTTPException 404: If artifact not found
        HTTPException 403: If user doesn't have access to artifact
    """
    # Fetch artifact
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()

    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact {artifact_id} not found"
        )

    # Verify tenant access via work order
    work_order = db.query(WorkOrder).filter(WorkOrder.id == artifact.work_order_id).first()

    if not work_order or work_order.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this artifact"
        )

    return ArtifactResponse.model_validate(artifact)


@router.get("/{artifact_id}/download")
async def download_artifact(
    artifact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    """
    Download an artifact file.

    Args:
        artifact_id: Artifact ID
        current_user: Authenticated user
        db: Database session

    Returns:
        File download response

    Raises:
        HTTPException 404: If artifact not found or file doesn't exist
        HTTPException 403: If user doesn't have access to artifact
    """
    # Fetch artifact
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()

    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact {artifact_id} not found"
        )

    # Verify tenant access via work order
    work_order = db.query(WorkOrder).filter(WorkOrder.id == artifact.work_order_id).first()

    if not work_order or work_order.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this artifact"
        )

    # Check if file exists
    if not os.path.exists(artifact.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact file not found at {artifact.file_path}"
        )

    # Determine media type
    media_type = artifact.mime_type or "application/octet-stream"

    # Return file for download
    return FileResponse(
        path=artifact.file_path,
        media_type=media_type,
        filename=artifact.artifact_name,
        headers={
            "Content-Disposition": f'attachment; filename="{artifact.artifact_name}"',
            "X-Artifact-ID": str(artifact.id),
            "X-Checksum-SHA256": artifact.checksum_sha256,
        }
    )


@router.get("/work-order/{work_order_id}", response_model=List[ArtifactResponse])
async def list_work_order_artifacts(
    work_order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[ArtifactResponse]:
    """
    List all artifacts for a work order.

    Args:
        work_order_id: Work order ID
        current_user: Authenticated user
        db: Database session

    Returns:
        List of artifacts

    Raises:
        HTTPException 404: If work order not found
        HTTPException 403: If user doesn't have access to work order
    """
    # Verify work order exists and user has access
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id,
        WorkOrder.tenant_id == current_user.tenant_id
    ).first()

    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order {work_order_id} not found"
        )

    # Fetch artifacts
    artifacts = db.query(Artifact).filter(
        Artifact.work_order_id == work_order_id
    ).order_by(Artifact.created_at.desc()).all()

    return [ArtifactResponse.model_validate(artifact) for artifact in artifacts]
