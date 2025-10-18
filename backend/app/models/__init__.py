"""Database models package.

All models are eagerly imported to ensure SQLAlchemy can resolve
foreign key relationships at runtime.
"""

# Eager imports - import all models upfront
# This ensures SQLAlchemy metadata is complete before any queries
from app.models.tenant import Tenant
from app.models.user import User
from app.models.file_upload import FileUpload
from app.models.dataset import Dataset
from app.models.mapping_config import MappingConfig
from app.models.policy_pack import PolicyPack
from app.models.work_order import WorkOrder
from app.models.audit_event import AuditEvent
from app.models.artifact import Artifact

__all__ = [
    "Tenant",
    "User",
    "FileUpload",
    "Dataset",
    "MappingConfig",
    "PolicyPack",
    "WorkOrder",
    "AuditEvent",
    "Artifact",
]
