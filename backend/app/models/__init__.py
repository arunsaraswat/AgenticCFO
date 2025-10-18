"""Database models package."""

# Lazy imports to avoid circular dependencies
# Import models only when explicitly accessed
__all__ = [
    "Artifact",
    "AuditEvent",
    "Dataset",
    "FileUpload",
    "MappingConfig",
    "PolicyPack",
    "Tenant",
    "User",
    "WorkOrder",
]


def __getattr__(name):
    """Lazy import models to avoid circular imports."""
    if name == "Artifact":
        from app.models.artifact import Artifact
        return Artifact
    elif name == "AuditEvent":
        from app.models.audit_event import AuditEvent
        return AuditEvent
    elif name == "Dataset":
        from app.models.dataset import Dataset
        return Dataset
    elif name == "FileUpload":
        from app.models.file_upload import FileUpload
        return FileUpload
    elif name == "MappingConfig":
        from app.models.mapping_config import MappingConfig
        return MappingConfig
    elif name == "PolicyPack":
        from app.models.policy_pack import PolicyPack
        return PolicyPack
    elif name == "Tenant":
        from app.models.tenant import Tenant
        return Tenant
    elif name == "User":
        from app.models.user import User
        return User
    elif name == "WorkOrder":
        from app.models.work_order import WorkOrder
        return WorkOrder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
