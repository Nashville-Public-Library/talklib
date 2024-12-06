import os

from src.tests.mock import env_vars

def pytest_sessionstart(session):
    for key, value in env_vars.items():
        os.environ[key] = value