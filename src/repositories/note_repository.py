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
Note Repository - Data access layer for Session Note entities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.note import Note
from src.repositories.base import BaseRepository

__version__ = "v5.0-2-2.5-1"


class NoteRepository(BaseRepository[Note, UUID]):
    """
    Repository for Note entity operations.

    Provides CRUD operations plus note-specific queries like
    getting notes by session, author, and handling version tracking.
    """

    def __init__(self, db_manager, logging_manager):
        """
        Initialize NoteRepository.

        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        super().__init__(Note, db_manager, logging_manager)

    # =========================================================================
    # Note Queries by Session
    # =========================================================================

    async def get_by_session(
        self,
        session: AsyncSession,
        session_id: str,
        include_author: bool = False,
    ) -> List[Note]:
        """
        Get all notes for a session.

        Args:
            session: Database session
            session_id: Crisis session ID
            include_author: If True, eagerly load author relationship

        Returns:
            List of notes ordered by creation time
        """
        query = (
            select(Note)
            .where(Note.session_id == session_id)
            .order_by(Note.created_at.asc())
        )
        
        if include_author:
            query = query.options(selectinload(Note.author))
        
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_latest_by_session(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Note]:
        """
        Get the most recent note for a session.

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            Most recent note or None
        """
        query = (
            select(Note)
            .where(Note.session_id == session_id)
            .order_by(Note.created_at.desc())
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def count_by_session(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> int:
        """
        Count notes for a session.

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            Number of notes
        """
        return await self.count(session, {"session_id": session_id})

    # =========================================================================
    # Note Queries by Author
    # =========================================================================

    async def get_by_author(
        self,
        session: AsyncSession,
        author_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Note]:
        """
        Get all notes by an author.

        Args:
            session: Database session
            author_id: Author user UUID
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of notes by the author
        """
        return await self.get_filtered(
            session,
            filters={"author_id": author_id},
            skip=skip,
            limit=limit,
            order_by="created_at",
            descending=True,
        )

    async def count_by_author(
        self,
        session: AsyncSession,
        author_id: UUID,
    ) -> int:
        """
        Count notes by an author.

        Args:
            session: Database session
            author_id: Author user UUID

        Returns:
            Number of notes
        """
        return await self.count(session, {"author_id": author_id})

    # =========================================================================
    # Note Creation and Updates
    # =========================================================================

    async def create_note(
        self,
        session: AsyncSession,
        session_id: str,
        author_id: UUID,
        content: str,
        content_html: Optional[str] = None,
    ) -> Note:
        """
        Create a new note for a session.

        Args:
            session: Database session
            session_id: Crisis session ID
            author_id: Author user UUID
            content: Note content (markdown)
            content_html: Optional pre-rendered HTML

        Returns:
            Created note
        """
        note_data = {
            "session_id": session_id,
            "author_id": author_id,
            "content": content,
            "content_html": content_html,
            "version": 1,
            "is_locked": False,
        }
        return await self.create(session, note_data)

    async def update_content(
        self,
        session: AsyncSession,
        note_id: UUID,
        content: str,
        content_html: Optional[str] = None,
    ) -> Optional[Note]:
        """
        Update a note's content and increment version.

        Args:
            session: Database session
            note_id: Note UUID
            content: New content
            content_html: Optional new rendered HTML

        Returns:
            Updated note or None if not found or locked
        """
        note = await self.get(session, note_id)
        if not note:
            return None
        
        if note.is_locked:
            self._logger.warning(f"Attempted to update locked note {note_id}")
            return None
        
        updates = {
            "content": content,
            "content_html": content_html,
            "version": note.version + 1,
            "updated_at": datetime.now(timezone.utc),
        }
        
        return await self.update(session, note_id, updates)

    # =========================================================================
    # Note Locking
    # =========================================================================

    async def lock_note(
        self,
        session: AsyncSession,
        note_id: UUID,
    ) -> Optional[Note]:
        """
        Lock a note to prevent further edits.

        Args:
            session: Database session
            note_id: Note UUID

        Returns:
            Updated note or None if not found
        """
        return await self.update(session, note_id, {"is_locked": True})

    async def unlock_note(
        self,
        session: AsyncSession,
        note_id: UUID,
    ) -> Optional[Note]:
        """
        Unlock a note to allow edits.

        Args:
            session: Database session
            note_id: Note UUID

        Returns:
            Updated note or None if not found
        """
        return await self.update(session, note_id, {"is_locked": False})

    async def lock_session_notes(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> int:
        """
        Lock all notes for a session.

        Typically called when a session is closed.

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            Number of notes locked
        """
        return await self.update_many(
            session,
            filters={"session_id": session_id},
            values={"is_locked": True},
        )

    # =========================================================================
    # Note Search
    # =========================================================================

    async def search_notes(
        self,
        session: AsyncSession,
        query: str,
        session_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Note]:
        """
        Search notes by content.

        Args:
            session: Database session
            query: Search string
            session_id: Optional session filter
            limit: Maximum results

        Returns:
            List of matching notes
        """
        search_pattern = f"%{query}%"
        stmt = select(Note).where(Note.content.ilike(search_pattern))
        
        if session_id:
            stmt = stmt.where(Note.session_id == session_id)
        
        stmt = stmt.order_by(Note.created_at.desc()).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    # =========================================================================
    # Note Statistics
    # =========================================================================

    async def get_author_statistics(
        self,
        session: AsyncSession,
        author_id: UUID,
    ) -> Dict[str, Any]:
        """
        Get note statistics for an author.

        Args:
            session: Database session
            author_id: Author user UUID

        Returns:
            Dictionary of statistics
        """
        # Total notes
        total = await self.count_by_author(session, author_id)
        
        # Notes by session count
        session_count_query = (
            select(func.count(func.distinct(Note.session_id)))
            .where(Note.author_id == author_id)
        )
        session_result = await session.execute(session_count_query)
        unique_sessions = session_result.scalar() or 0
        
        return {
            "total_notes": total,
            "unique_sessions": unique_sessions,
            "average_per_session": round(total / unique_sessions, 2) if unique_sessions > 0 else 0,
        }


def create_note_repository(db_manager, logging_manager) -> NoteRepository:
    """
    Factory function for NoteRepository.

    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured NoteRepository instance
    """
    return NoteRepository(db_manager, logging_manager)


__all__ = ["NoteRepository", "create_note_repository"]
