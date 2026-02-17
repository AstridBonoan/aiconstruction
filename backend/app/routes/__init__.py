"""API routes."""

from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.routes import health, projects, dashboard, risk, dependencies, auth, sync, webhooks
