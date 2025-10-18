"""User database model."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant


class User(Base):
    """
    User model for authentication and user management.

    Attributes:
        id: Unique identifier
        email: User email (unique)
        full_name: User's full name
        hashed_password: Bcrypt hashed password
        tenant_id: Foreign key to tenant (multi-tenancy)
        role: User role (admin, manager, analyst, viewer)
        approval_authority: Max USD amount user can approve
        is_active: Whether the user account is active
        is_superuser: Whether the user has admin privileges
        created_at: Timestamp of account creation
        updated_at: Timestamp of last update

    Relationships:
        tenant: Tenant that owns this user
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False, default="analyst")  # admin, manager, analyst, viewer
    approval_authority = Column(Integer, nullable=False, default=0)  # Max USD amount user can approve
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships (commented out to avoid circular import issues)
    # tenant = relationship("Tenant", back_populates="users")

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.full_name}', role='{self.role}')>"
