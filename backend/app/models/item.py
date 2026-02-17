"""Item model - mirrors Monday.com board item (task/phase)."""

from datetime import datetime, date
from app.extensions import db


class Item(db.Model):
    """Monday.com board item - task, phase, or deliverable."""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"), nullable=False, index=True)
    monday_item_id = db.Column(db.String(64), nullable=True, index=True)
    name = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(64), default="new")  # new, working_on, done, stuck
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completion_percent = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ItemDependency(db.Model):
    """Dependency between items - blocks/blocked_by."""

    __tablename__ = "item_dependencies"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False, index=True)
    depends_on_item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
