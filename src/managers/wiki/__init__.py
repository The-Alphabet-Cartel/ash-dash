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
Wiki Managers Package - Documentation wiki management
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.1-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

COMPONENTS:
- WikiManager: Core wiki management (scan, parse, search)
- Models: Pydantic models for documents, navigation, search results
- (Future) MarkdownRenderer: Markdown to HTML conversion with syntax highlighting
- (Future) PDFGenerator: PDF export via WeasyPrint

USAGE:
    from src.managers.wiki import create_wiki_manager, WikiDocument
    
    wiki = create_wiki_manager(config_manager, logging_manager)
    docs = wiki.scan_documents()
    doc = wiki.get_document("crt/crisis-response-guide")
"""

__version__ = "v5.0-7-7.1-1"

# Core manager
from .wiki_manager import WikiManager, create_wiki_manager

# Models
from .models import (
    # Core document models
    WikiDocument,
    WikiDocumentSummary,
    WikiTocEntry,
    # Search models
    WikiSearchResult,
    # Navigation models
    WikiNavItem,
    WikiNavCategory,
    WikiNavigation,
    # Category/Tag models
    WikiCategory,
    WikiTag,
    # Response models
    WikiDocumentListResponse,
    WikiSearchResponse,
)

__all__ = [
    # Manager
    "WikiManager",
    "create_wiki_manager",
    # Core models
    "WikiDocument",
    "WikiDocumentSummary",
    "WikiTocEntry",
    # Search models
    "WikiSearchResult",
    # Navigation models
    "WikiNavItem",
    "WikiNavCategory",
    "WikiNavigation",
    # Category/Tag models
    "WikiCategory",
    "WikiTag",
    # Response models
    "WikiDocumentListResponse",
    "WikiSearchResponse",
]
