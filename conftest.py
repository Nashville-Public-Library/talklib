import os
from unittest.mock import patch, Mock
import pytest
from src.tests.mock import env_vars

# Patch Notify BEFORE any TLShow instance is created
@pytest.fixture(autouse=True)
def mock_notify(monkeypatch):
    # Patch the Notify class so that it doesn't instantiate anything
    # This ensures that every Notify() created is a mock
    with patch("talklib.notify.Notify", new=Mock()) as mock_notify:
        yield mock_notify

# Environment setup
def pytest_sessionstart(session):
    for key, value in env_vars.items():
        os.environ[key] = value