"""Integration tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


@pytest.mark.integration
class TestAuthEndpoints:
    """Test authentication API endpoints."""

    def test_register_user_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "securepass123",
                "full_name": "New User"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "message" in data
        assert "id" in data

    def test_register_user_duplicate_email(self, client: TestClient, test_user: User):
        """Test registration with existing email."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,
                "password": "password123",
                "full_name": "Duplicate User"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_user_invalid_email(self, client: TestClient):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalidemail",
                "password": "password123",
                "full_name": "Test User"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_register_user_short_password(self, client: TestClient):
        """Test registration with password too short."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
                "full_name": "Test User"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login with incorrect password."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 401

    def test_login_inactive_user(self, client: TestClient, db: Session):
        """Test login with inactive user."""
        # Create inactive user
        inactive_user = User(
            email="inactive@example.com",
            full_name="Inactive User",
            hashed_password="hashed_pass",
            is_active=False
        )
        db.add(inactive_user)
        db.commit()

        response = client.post(
            "/api/auth/login",
            json={
                "email": "inactive@example.com",
                "password": "password123"
            }
        )

        # Should fail authentication
        assert response.status_code in [400, 401]
