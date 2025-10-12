"""Integration tests for user endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


@pytest.mark.integration
class TestUserEndpoints:
    """Test user API endpoints."""

    def test_get_profile_success(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test getting user profile with authentication."""
        response = client.get("/api/users/profile", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["full_name"] == test_user.full_name
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    def test_get_profile_no_auth(self, client: TestClient):
        """Test getting profile without authentication."""
        response = client.get("/api/users/profile")

        assert response.status_code == 401

    def test_get_profile_invalid_token(self, client: TestClient):
        """Test getting profile with invalid token."""
        response = client.get(
            "/api/users/profile",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401
