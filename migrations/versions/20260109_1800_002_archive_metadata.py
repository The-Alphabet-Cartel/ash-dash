"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Add queryable metadata columns to archives table

Revision ID: 002_archive_metadata
Revises: 001_initial
Create Date: 2026-01-09
Phase: Phase 9 - Archive System Implementation
============================================================================

Changes:
- Add retention_tier column (standard/permanent)
- Add discord_user_id and discord_user_name columns
- Add severity column
- Add notes_count column
- Add archived_by_name column (denormalized for display)
- Add session_started_at and session_ended_at columns
- Add new indexes for filtering performance
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision: str = "002_archive_metadata"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add queryable metadata columns to archives table."""
    
    # =========================================================================
    # Add new columns
    # =========================================================================
    
    # Retention tier: "standard" (1 year) or "permanent" (7 years)
    op.add_column(
        "archives",
        sa.Column(
            "retention_tier",
            sa.String(20),
            nullable=False,
            server_default="standard",
        ),
    )
    
    # Discord user whose session was archived
    op.add_column(
        "archives",
        sa.Column("discord_user_id", sa.BigInteger, nullable=True),
    )
    
    op.add_column(
        "archives",
        sa.Column("discord_user_name", sa.String(100), nullable=True),
    )
    
    # Crisis severity level
    op.add_column(
        "archives",
        sa.Column("severity", sa.String(20), nullable=True),
    )
    
    # Number of notes included in archive
    op.add_column(
        "archives",
        sa.Column("notes_count", sa.Integer, nullable=False, server_default="0"),
    )
    
    # Display name of CRT member who archived (denormalized)
    op.add_column(
        "archives",
        sa.Column("archived_by_name", sa.String(100), nullable=True),
    )
    
    # Original session timestamps
    op.add_column(
        "archives",
        sa.Column("session_started_at", sa.DateTime(timezone=True), nullable=True),
    )
    
    op.add_column(
        "archives",
        sa.Column("session_ended_at", sa.DateTime(timezone=True), nullable=True),
    )
    
    # =========================================================================
    # Add check constraint for retention_tier
    # =========================================================================
    op.create_check_constraint(
        "ck_archives_valid_retention_tier",
        "archives",
        "retention_tier IN ('standard', 'permanent')",
    )
    
    # =========================================================================
    # Create indexes for new columns
    # =========================================================================
    op.create_index("ix_archives_retention_tier", "archives", ["retention_tier"])
    op.create_index("ix_archives_discord_user", "archives", ["discord_user_id"])
    op.create_index("ix_archives_severity", "archives", ["severity"])
    
    # Composite index for common filter combinations
    op.create_index(
        "ix_archives_filter_combo",
        "archives",
        ["severity", "retention_tier", "archived_at"],
    )
    
    # Composite index for retention queries
    op.create_index(
        "ix_archives_retention",
        "archives",
        ["retention_tier", "retention_until"],
    )
    
    # =========================================================================
    # Migrate existing data from extra_data JSONB
    # =========================================================================
    # This updates existing archives (if any) to populate new columns
    # from their extra_data JSON field
    op.execute("""
        UPDATE archives
        SET 
            retention_tier = COALESCE(
                extra_data->>'retention_tier',
                'standard'
            ),
            discord_user_id = (extra_data->>'user_id')::bigint,
            discord_user_name = extra_data->>'user_name',
            severity = extra_data->>'severity',
            notes_count = COALESCE((extra_data->>'notes_count')::integer, 0),
            archived_by_name = extra_data->>'archived_by_name',
            session_started_at = (extra_data->>'session_start')::timestamptz,
            session_ended_at = (extra_data->>'session_end')::timestamptz
        WHERE extra_data IS NOT NULL
    """)


def downgrade() -> None:
    """Remove queryable metadata columns from archives table."""
    
    # Drop indexes first
    op.drop_index("ix_archives_retention", table_name="archives")
    op.drop_index("ix_archives_filter_combo", table_name="archives")
    op.drop_index("ix_archives_severity", table_name="archives")
    op.drop_index("ix_archives_discord_user", table_name="archives")
    op.drop_index("ix_archives_retention_tier", table_name="archives")
    
    # Drop constraint
    op.drop_constraint("ck_archives_valid_retention_tier", "archives", type_="check")
    
    # Drop columns
    op.drop_column("archives", "session_ended_at")
    op.drop_column("archives", "session_started_at")
    op.drop_column("archives", "archived_by_name")
    op.drop_column("archives", "notes_count")
    op.drop_column("archives", "severity")
    op.drop_column("archives", "discord_user_name")
    op.drop_column("archives", "discord_user_id")
    op.drop_column("archives", "retention_tier")
