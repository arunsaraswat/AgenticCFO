"""Database base configuration."""
from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

# Import all models here to ensure they are registered with Base
# This is required for Alembic migrations to detect all tables
from app.models import (  # noqa: F401, E402
    Artifact,
    AuditEvent,
    Dataset,
    FileUpload,
    MappingConfig,
    PolicyPack,
    Tenant,
    User,
    WorkOrder,
)
