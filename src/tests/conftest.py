import pytest

from .mock import env_vars

@pytest.fixture(autouse=True, scope="function")
def mock_env_vars(monkeypatch):
    # Mock the 'destinations' environment variable globally
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
