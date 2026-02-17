"""Application configuration."""

import os
from typing import Optional


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
    MONDAY_CLIENT_ID = os.environ.get("MONDAY_CLIENT_ID", "")
    MONDAY_CLIENT_SECRET = os.environ.get("MONDAY_CLIENT_SECRET", "")
    MONDAY_OAUTH_REDIRECT_URI = os.environ.get(
        "MONDAY_OAUTH_REDIRECT_URI", "http://localhost:8000/api/v1/auth/monday/callback"
    )
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
    MONDAY_OAUTH_SCOPES = "boards:read boards:write account:read me:read webhooks:read webhooks:write"


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/construction_ai"
    )


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///:memory:"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
