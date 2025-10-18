"""Pytest configuration for artifact tests."""
import pytest


# Minimal conftest that doesn't import the full app
# This avoids langchain/pydantic compatibility issues for artifact-only tests
@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary directory for test outputs."""
    return tmp_path
