"""Tenant model for multi-tenant architecture."""

from datetime import datetime
from app.extensions import db


class Tenant(db.Model):
    """Workspace/tenant - maps to Monday.com account."""

    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    monday_account_id = db.Column(db.String(64), unique=True, nullable=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
