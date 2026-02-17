"""Board model - mirrors Monday.com board structure."""

from datetime import datetime
from app.extensions import db


class Board(db.Model):
    """Monday.com board - construction project container."""

    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False, index=True)
    monday_board_id = db.Column(db.String(64), nullable=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    board_type = db.Column(db.String(64), default="project")  # project, portfolio, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
