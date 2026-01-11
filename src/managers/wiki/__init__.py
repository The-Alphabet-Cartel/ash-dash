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
FILE VERSION: v5.0-7-7.8-2
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

COMPONENTS:
- WikiManager: Core wiki management (scan, parse, search, PDF)
- MarkdownRenderer: Markdown to HTML conversion with syntax highlighting
- PDFGenerator: PDF export via WeasyPrint
- Models: Pydantic models for documents, navigation, search results

USAGE:
    from src.managers.wiki import create_wiki_manager, WikiDocument
    
    wiki = create_wiki_manager(config_manager, logging_manager)
    docs = wiki.scan_documents()
    doc = wiki.get_rendered_document("crt/crisis-response-guide")
    
    # Generate PDF
    if wiki.is_pdf_available():
        pdf_bytes = wiki.generate_pdf("crt/crisis-response-guide")
    
    # Or use renderer/generator directly
    from src.managers.wiki import create_markdown_renderer, create_pdf_generator
    renderer = create_markdown_renderer()
    generator = create_pdf_generator()
"""

__version__ = "v5.0-7-7.8-2"

# Core manager
from .wiki_manager import WikiManager, create_wiki_manager

# Markdown renderer
from .markdown_renderer import (
    MarkdownRenderer,
    create_markdown_renderer,
    get_wiki_styles,
    get_pygments_styles,
)

# PDF generator
from .pdf_generator import (
    PDFGenerator,
    create_pdf_generator,
    PDF_STYLES,
)

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
    # Managers
    "WikiManager",
    "create_wiki_manager",
    # Markdown renderer
    "MarkdownRenderer",
    "create_markdown_renderer",
    "get_wiki_styles",
    "get_pygments_styles",
    # PDF generator
    "PDFGenerator",
    "create_pdf_generator",
    "PDF_STYLES",
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
