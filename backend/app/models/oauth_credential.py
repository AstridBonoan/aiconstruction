"""OAuth credential storage - tokens per tenant."""

from datetime import datetime
from app.extensions import db


class OAuthCredential(db.Model):
    """Monday.com OAuth tokens per tenant."""

    __tablename__ = "oauth_credentials"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False, unique=True, index=True)
    access_token_enc = db.Column(db.LargeBinary, nullable=False)  # Encrypted in Phase 2 token-encryption
    account_id = db.Column(db.String(64), nullable=True, index=True)  # Monday account ID
    scope = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
