"""Initial schema - tenants, boards, items, dependencies, risk_scores.

Revision ID: 001
Revises:
Create Date: 2025-02-17

"""
from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None


def upgrade():
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("monday_account_id", sa.String(64), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tenants_monday_account_id", "tenants", ["monday_account_id"], unique=True)

    op.create_table(
        "boards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("monday_board_id", sa.String(64), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("board_type", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
    )
    op.create_index("ix_boards_tenant_id", "boards", ["tenant_id"])
    op.create_index("ix_boards_monday_board_id", "boards", ["monday_board_id"])

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("monday_item_id", sa.String(64), nullable=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("status", sa.String(64), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("completion_percent", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
    )
    op.create_index("ix_items_board_id", "items", ["board_id"])
    op.create_index("ix_items_monday_item_id", "items", ["monday_item_id"])

    op.create_table(
        "item_dependencies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("depends_on_item_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"]),
        sa.ForeignKeyConstraint(["depends_on_item_id"], ["items.id"]),
    )
    op.create_index("ix_item_dependencies_item_id", "item_dependencies", ["item_id"])
    op.create_index("ix_item_dependencies_depends_on_item_id", "item_dependencies", ["depends_on_item_id"])

    op.create_table(
        "risk_scores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=True),
        sa.Column("item_id", sa.Integer(), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("level", sa.String(32), nullable=False),
        sa.Column("factors", sa.JSON(), nullable=True),
        sa.Column("calculated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"]),
    )
    op.create_index("ix_risk_scores_tenant_id", "risk_scores", ["tenant_id"])
    op.create_index("ix_risk_scores_board_id", "risk_scores", ["board_id"])
    op.create_index("ix_risk_scores_item_id", "risk_scores", ["item_id"])


def downgrade():
    op.drop_table("risk_scores")
    op.drop_table("item_dependencies")
    op.drop_table("items")
    op.drop_table("boards")
    op.drop_table("tenants")
