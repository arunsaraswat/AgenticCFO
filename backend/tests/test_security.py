"""Unit tests for security utilities."""
import pytest
from datetime import timedelta

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)


@pytest.mark.unit
class TestSecurity:
    """Test security functions."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "mysecurepassword"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_create_and_decode_token(self):
        """Test JWT token creation and decoding."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert token is not None
        decoded_username = decode_access_token(token)
        assert decoded_username == "test@example.com"

    def test_token_with_custom_expiration(self):
        """Test token with custom expiration time."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(minutes=60))

        assert token is not None
        decoded_username = decode_access_token(token)
        assert decoded_username == "test@example.com"

    def test_invalid_token_decode(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"
        result = decode_access_token(invalid_token)

        assert result is None

    def test_different_passwords_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "testpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
