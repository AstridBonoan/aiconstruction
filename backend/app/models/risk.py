"""Risk score model."""

from datetime import datetime
from app.extensions import db


class RiskScore(db.Model):
    """Risk score for board or item."""

    __tablename__ = "risk_scores"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False, index=True)
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"), nullable=True, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True, index=True)
    score = db.Column(db.Float, nullable=False)  # 0-100
    level = db.Column(db.String(32), nullable=False)  # low, medium, high, critical
    factors = db.Column(db.JSON, default=dict)  # contributing factors
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
