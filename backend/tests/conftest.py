"""Pytest configuration."""

import pytest


@pytest.fixture
def app():
    from app import create_app
    return create_app("testing")
