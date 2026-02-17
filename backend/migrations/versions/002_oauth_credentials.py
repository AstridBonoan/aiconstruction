"""Add oauth_credentials table.

Revision ID: 002
Revises: 001
Create Date: 2025-02-17

"""
from alembic import op
import sqlalchemy as sa


revision = "002"
down_revision = "001"


def upgrade():
    op.create_table(
        "oauth_credentials",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("access_token_enc", sa.LargeBinary(), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=True),
        sa.Column("scope", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
    )
    op.create_index("ix_oauth_credentials_tenant_id", "oauth_credentials", ["tenant_id"], unique=True)
    op.create_index("ix_oauth_credentials_account_id", "oauth_credentials", ["account_id"])


def downgrade():
    op.drop_table("oauth_credentials")
