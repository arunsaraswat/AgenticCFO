"""Unit tests for database models."""
import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.core.security import get_password_hash


@pytest.mark.unit
class TestUserModel:
    """Test User model."""

    def test_create_user(self, db: Session):
        """Test creating a user."""
        user = User(
            email="newuser@example.com",
            full_name="New User",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.is_active is True
        assert user.is_superuser is False
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_email_unique(self, db: Session, test_user: User):
        """Test that email must be unique."""
        duplicate_user = User(
            email=test_user.email,
            full_name="Duplicate User",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=False
        )
        db.add(duplicate_user)

        with pytest.raises(Exception):  # Should raise IntegrityError
            db.commit()

    def test_user_repr(self, test_user: User):
        """Test user string representation."""
        repr_string = repr(test_user)
        assert "Test User" in repr_string
        assert "test@example.com" in repr_string

    def test_user_defaults(self, db: Session):
        """Test user default values."""
        user = User(
            email="defaults@example.com",
            full_name="Defaults User",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.is_active is True
        assert user.is_superuser is False
        assert user.created_at is not None
        assert user.updated_at is not None
