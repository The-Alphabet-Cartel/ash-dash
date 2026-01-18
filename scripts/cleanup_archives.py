#!/usr/bin/env python3
"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
Archive Cleanup Script - Delete expired standard-tier archives
----------------------------------------------------------------------------
FILE VERSION: v5.0-9-9.9-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
    # Run cleanup (dry-run by default)
    docker exec ash-dash python scripts/cleanup_archives.py

    # Run actual cleanup
    docker exec ash-dash python scripts/cleanup_archives.py --execute

    # Show archives expiring in next N days
    docker exec ash-dash python scripts/cleanup_archives.py --expiring 30

SCHEDULING:
    Add to crontab on host machine:
    # Run daily at 3:00 AM
    0 3 * * * docker exec ash-dash python scripts/cleanup_archives.py --execute >> /var/log/ash-dash-cleanup.log 2>&1

NOTES:
    - Only deletes "standard" tier archives past retention_until date
    - "permanent" tier archives are NEVER auto-deleted
    - Creates audit log entries for each deletion
"""

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.managers.config import create_config_manager
from src.managers.secrets import SecretsManager
from src.managers.logging_config_manager import create_logging_config_manager
from src.managers.database import create_database_manager
from src.managers.archive import create_minio_manager, create_archive_manager
from src.repositories.archive_repository import create_archive_repository


__version__ = "v5.0-9-9.9-1"


async def run_cleanup(execute: bool = False, expiring_days: int = None):
    """
    Run archive cleanup process.

    Args:
        execute: If True, actually delete archives. If False, dry-run only.
        expiring_days: If set, show archives expiring within N days instead of cleanup.
    """
    print("=" * 60)
    print("Ash-Dash Archive Cleanup")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    print()

    # Initialize managers
    print("🔧 Initializing managers...")

    try:
        config_manager = create_config_manager()
        secrets_manager = SecretsManager()
        logging_manager = create_logging_manager(config_manager)
        logger = logging_manager.get_logger("cleanup")

        # Check for archive key
        if not secrets_manager.has_archive_master_key():
            print("❌ Archive master key not configured!")
            print("   Run: docker exec ash-dash python scripts/generate_archive_key.py")
            return 1

        # Create database manager
        db_manager = await create_database_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            logging_manager=logging_manager,
        )

        # Create MinIO manager
        minio_manager = await create_minio_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            logging_manager=logging_manager,
        )

        # Create archive repository and manager
        archive_repo = create_archive_repository(db_manager, logging_manager)
        archive_manager = await create_archive_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            minio_manager=minio_manager,
            database_manager=db_manager,
            archive_repository=archive_repo,
            logging_manager=logging_manager,
        )

        print("✅ All managers initialized")
        print()

        # Mode: Show expiring archives
        if expiring_days is not None:
            print(f"📅 Archives expiring within {expiring_days} days:")
            print("-" * 60)

            expiring = await archive_manager.get_expiring_soon(days=expiring_days)

            if not expiring:
                print("   No archives expiring in this period.")
            else:
                for archive in expiring:
                    print(f"   • {archive['session_id']}")
                    print(f"     User: {archive['discord_user_name']}")
                    print(
                        f"     Expires: {archive['retention_until']} ({archive['days_remaining']}d)"
                    )
                    print()

                print(f"Total: {len(expiring)} archive(s) expiring")

            return 0

        # Mode: Cleanup
        # Get statistics first
        stats = await archive_manager.get_statistics()
        print("📊 Current Archive Statistics:")
        print(f"   Total archives: {stats.get('total_archives', 0)}")
        print(f"   Total size: {stats.get('total_size_mb', 0):.2f} MB")
        print()

        # Get expired archives count
        async with db_manager.session() as db:
            expired = await archive_repo.get_expired_standard_tier(db, limit=1000)
            expired_count = len(list(expired))

        print(f"🗑️  Expired standard-tier archives: {expired_count}")
        print()

        if expired_count == 0:
            print("✅ No expired archives to clean up!")
            return 0

        if not execute:
            print("⚠️  DRY RUN MODE - No archives will be deleted")
            print("   To actually delete, run with --execute flag")
            print()

            # Show what would be deleted
            print("Archives that would be deleted:")
            print("-" * 60)
            async with db_manager.session() as db:
                expired = await archive_repo.get_expired_standard_tier(db, limit=100)
                for archive in expired:
                    print(f"   • {archive.session_id}")
                    print(f"     User: {archive.discord_user_name}")
                    print(f"     Archived: {archive.archived_at}")
                    print(f"     Expired: {archive.retention_until}")
                    print()

            return 0

        # Execute cleanup
        print("🚀 EXECUTING CLEANUP...")
        print("-" * 60)

        deleted_count = await archive_manager.delete_expired_archives()

        print()
        print("=" * 60)
        print(f"✅ Cleanup complete!")
        print(f"   Archives deleted: {deleted_count}")
        print(f"   Finished: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 60)

        logger.info(f"Archive cleanup completed: {deleted_count} archives deleted")

        return 0

    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        if "db_manager" in locals():
            await db_manager.close()
        if "minio_manager" in locals():
            await minio_manager.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ash-Dash Archive Cleanup - Delete expired standard-tier archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (shows what would be deleted)
  python scripts/cleanup_archives.py

  # Actually delete expired archives
  python scripts/cleanup_archives.py --execute

  # Show archives expiring in next 30 days
  python scripts/cleanup_archives.py --expiring 30

  # Show archives expiring in next 7 days
  python scripts/cleanup_archives.py --expiring 7
        """,
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete archives (default is dry-run)",
    )

    parser.add_argument(
        "--expiring",
        type=int,
        metavar="DAYS",
        help="Show archives expiring within N days (no deletion)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    # Run async cleanup
    exit_code = asyncio.run(
        run_cleanup(
            execute=args.execute,
            expiring_days=args.expiring,
        )
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
