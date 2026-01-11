"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Initial schema - Creates all Phase 2 tables

Revision ID: 001_initial
Revises: None
Create Date: 2026-01-07
============================================================================

Tables created:
- users: CRT members and administrators
- sessions: Crisis sessions from Ash-Bot
- notes: Session documentation by CRT members
- archives: Encrypted MinIO storage references
- audit_log: Administrative action logging
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all initial tables."""
    
    # =========================================================================
    # USERS TABLE
    # =========================================================================
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("pocket_id_sub", sa.String(255), unique=True, nullable=True),
        sa.Column("groups", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("role", sa.String(20), nullable=False, server_default="crt_member"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        comment="CRT members and administrators",
    )
    
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_pocket_id", "users", ["pocket_id_sub"])
    
    # =========================================================================
    # SESSIONS TABLE
    # =========================================================================
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column(
            "crt_user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("discord_user_id", sa.BigInteger, nullable=False),
        sa.Column("discord_username", sa.String(100), nullable=True),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("crisis_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("confidence", sa.Numeric(5, 4), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer, nullable=True),
        sa.Column("message_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("ash_summary", sa.Text, nullable=True),
        sa.Column("analysis_data", postgresql.JSONB, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        comment="Crisis sessions from Ash-Bot",
    )
    
    op.create_index("ix_sessions_discord_user", "sessions", ["discord_user_id"])
    op.create_index("ix_sessions_status", "sessions", ["status"])
    op.create_index("ix_sessions_severity", "sessions", ["severity"])
    op.create_index("ix_sessions_started_at", "sessions", ["started_at"])
    op.create_index("ix_sessions_crt_user", "sessions", ["crt_user_id"])
    
    # =========================================================================
    # NOTES TABLE
    # =========================================================================
    op.create_table(
        "notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id",
            sa.String(50),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "author_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("content_html", sa.Text, nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("is_locked", sa.Boolean, nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.CheckConstraint("LENGTH(content) > 0", name="ck_notes_content_not_empty"),
        comment="Session documentation notes",
    )
    
    op.create_index("ix_notes_session", "notes", ["session_id"])
    op.create_index("ix_notes_author", "notes", ["author_id"])
    
    # =========================================================================
    # ARCHIVES TABLE
    # =========================================================================
    op.create_table(
        "archives",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id",
            sa.String(50),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("storage_key", sa.String(500), nullable=False),
        sa.Column(
            "storage_bucket",
            sa.String(100),
            nullable=False,
            server_default="ash-archives",
        ),
        sa.Column("encryption_iv", sa.LargeBinary, nullable=True),
        sa.Column("checksum", sa.String(64), nullable=False),
        sa.Column("size_bytes", sa.BigInteger, nullable=False),
        sa.Column(
            "archived_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "archived_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("retention_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("extra_data", postgresql.JSONB, nullable=True, server_default="{}"),
        sa.CheckConstraint("LENGTH(checksum) = 64", name="ck_archives_valid_checksum"),
        comment="Encrypted session archives in MinIO",
    )
    
    op.create_index("ix_archives_session", "archives", ["session_id"])
    op.create_index("ix_archives_date", "archives", ["archived_at"])
    
    # =========================================================================
    # AUDIT_LOG TABLE
    # =========================================================================
    op.create_table(
        "audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=True),
        sa.Column("entity_id", sa.String(100), nullable=True),
        sa.Column("old_values", postgresql.JSONB, nullable=True),
        sa.Column("new_values", postgresql.JSONB, nullable=True),
        sa.Column("ip_address", postgresql.INET, nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        comment="Administrative action audit log",
    )
    
    op.create_index("ix_audit_user", "audit_log", ["user_id"])
    op.create_index("ix_audit_action", "audit_log", ["action"])
    op.create_index("ix_audit_entity", "audit_log", ["entity_type", "entity_id"])
    op.create_index("ix_audit_created", "audit_log", ["created_at"])


def downgrade() -> None:
    """Drop all tables in reverse order."""
    
    # Drop in reverse order of creation (respect foreign keys)
    op.drop_table("audit_log")
    op.drop_table("archives")
    op.drop_table("notes")
    op.drop_table("sessions")
    op.drop_table("users")
