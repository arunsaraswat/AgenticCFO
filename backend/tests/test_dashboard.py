"""Integration tests for dashboard endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


@pytest.mark.integration
class TestDashboardEndpoints:
    """Test dashboard API endpoints."""

    def test_get_dashboard_success(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test getting dashboard data with authentication."""
        response = client.get("/api/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "stats" in data
        assert "message" in data
        assert data["user"]["email"] == test_user.email
        assert test_user.full_name in data["message"]

    def test_get_dashboard_no_auth(self, client: TestClient):
        """Test getting dashboard without authentication."""
        response = client.get("/api/dashboard")

        assert response.status_code == 401

    def test_get_dashboard_invalid_token(self, client: TestClient):
        """Test getting dashboard with invalid token."""
        response = client.get(
            "/api/dashboard",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    def test_dashboard_has_stats(self, client: TestClient, auth_headers: dict):
        """Test that dashboard returns statistics."""
        response = client.get("/api/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        stats = data["stats"]
        assert isinstance(stats, dict)
        # Check for expected stat keys (adjust based on actual implementation)
        assert len(stats) > 0
