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
Wiki Models - Pydantic models for wiki documentation system
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.1-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

MODELS:
- WikiDocument: Full document with content and metadata
- WikiDocumentSummary: Document listing without full content
- WikiSearchResult: Search result with score and snippet
- WikiNavigation: Navigation tree structure
- WikiCategory: Category with document count
- WikiTag: Tag with document count
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Module version
__version__ = "v5.0-7-7.1-1"


# =============================================================================
# Core Document Models
# =============================================================================


class WikiDocument(BaseModel):
    """
    Full wiki document with content and metadata.
    
    Represents a parsed Markdown file with extracted frontmatter.
    """
    
    # Identification
    slug: str = Field(..., description="URL-safe identifier (e.g., 'crt/crisis-response-guide')")
    file_path: str = Field(..., description="Absolute path to source file")
    
    # Frontmatter metadata
    title: str = Field(..., description="Document title from frontmatter or filename")
    description: str = Field(default="", description="Brief description from frontmatter")
    category: str = Field(default="general", description="Category from frontmatter or directory")
    tags: List[str] = Field(default_factory=list, description="List of tags from frontmatter")
    author: str = Field(default="Unknown", description="Author from frontmatter")
    version: str = Field(default="1.0", description="Document version from frontmatter")
    
    # Timestamps
    last_updated: Optional[str] = Field(default=None, description="Last updated date from frontmatter")
    file_modified: Optional[datetime] = Field(default=None, description="File system modification time")
    
    # Content
    content_md: str = Field(default="", description="Raw Markdown content (without frontmatter)")
    content_html: Optional[str] = Field(default=None, description="Rendered HTML content")
    
    # Table of contents (generated from headings)
    toc: List["WikiTocEntry"] = Field(default_factory=list, description="Table of contents entries")
    
    class Config:
        json_schema_extra = {
            "example": {
                "slug": "crt/crisis-response-guide",
                "file_path": "/app/docs/crt/crisis-response-guide.md",
                "title": "Crisis Response Guide",
                "description": "Comprehensive guide for CRT members",
                "category": "CRT Operations",
                "tags": ["crisis", "response", "procedures"],
                "author": "CRT Team",
                "version": "1.2",
                "last_updated": "2026-01-06",
                "content_md": "# Crisis Response Guide\n\nContent here...",
                "content_html": "<h1>Crisis Response Guide</h1><p>Content here...</p>",
            }
        }


class WikiTocEntry(BaseModel):
    """
    Table of contents entry representing a heading in the document.
    """
    
    level: int = Field(..., ge=1, le=6, description="Heading level (1-6)")
    text: str = Field(..., description="Heading text")
    anchor: str = Field(..., description="URL anchor for linking (e.g., 'getting-started')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "level": 2,
                "text": "Getting Started",
                "anchor": "getting-started",
            }
        }


class WikiDocumentSummary(BaseModel):
    """
    Document summary for listings (without full content).
    
    Used in document lists, search results, and navigation.
    """
    
    slug: str = Field(..., description="URL-safe identifier")
    title: str = Field(..., description="Document title")
    description: str = Field(default="", description="Brief description")
    category: str = Field(default="general", description="Document category")
    tags: List[str] = Field(default_factory=list, description="Document tags")
    author: str = Field(default="Unknown", description="Document author")
    last_updated: Optional[str] = Field(default=None, description="Last updated date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "slug": "crt/crisis-response-guide",
                "title": "Crisis Response Guide",
                "description": "Comprehensive guide for CRT members",
                "category": "CRT Operations",
                "tags": ["crisis", "response"],
                "author": "CRT Team",
                "last_updated": "2026-01-06",
            }
        }


# =============================================================================
# Search Models
# =============================================================================


class WikiSearchResult(BaseModel):
    """
    Search result with relevance score and content snippet.
    """
    
    document: WikiDocumentSummary = Field(..., description="Matched document summary")
    score: float = Field(..., ge=0, description="Relevance score (higher is better)")
    snippet: str = Field(default="", description="Content snippet with match context")
    match_locations: List[str] = Field(
        default_factory=list,
        description="Where matches were found (title, tags, content)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document": {
                    "slug": "crt/crisis-response-guide",
                    "title": "Crisis Response Guide",
                    "description": "Comprehensive guide for CRT members",
                    "category": "CRT Operations",
                    "tags": ["crisis", "response"],
                },
                "score": 15.5,
                "snippet": "...when handling a **crisis** situation, always...",
                "match_locations": ["title", "content"],
            }
        }


# =============================================================================
# Navigation Models
# =============================================================================


class WikiNavItem(BaseModel):
    """
    Single navigation item (document link).
    """
    
    slug: str = Field(..., description="Document slug")
    title: str = Field(..., description="Document title")
    
    class Config:
        json_schema_extra = {
            "example": {
                "slug": "crt/crisis-response-guide",
                "title": "Crisis Response Guide",
            }
        }


class WikiNavCategory(BaseModel):
    """
    Navigation category containing documents.
    """
    
    name: str = Field(..., description="Category name")
    slug: str = Field(..., description="Category slug (lowercase, hyphenated)")
    icon: Optional[str] = Field(default=None, description="Optional icon identifier")
    documents: List[WikiNavItem] = Field(default_factory=list, description="Documents in category")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "CRT Operations",
                "slug": "crt",
                "icon": "shield",
                "documents": [
                    {"slug": "crt/crisis-response-guide", "title": "Crisis Response Guide"},
                    {"slug": "crt/escalation-procedures", "title": "Escalation Procedures"},
                ],
            }
        }


class WikiNavigation(BaseModel):
    """
    Full navigation structure for sidebar.
    """
    
    categories: List[WikiNavCategory] = Field(
        default_factory=list,
        description="Navigation categories with documents"
    )
    total_documents: int = Field(default=0, description="Total document count")
    
    class Config:
        json_schema_extra = {
            "example": {
                "categories": [
                    {
                        "name": "Getting Started",
                        "slug": "getting-started",
                        "documents": [{"slug": "getting-started/overview", "title": "Overview"}],
                    }
                ],
                "total_documents": 12,
            }
        }


# =============================================================================
# Category & Tag Models
# =============================================================================


class WikiCategory(BaseModel):
    """
    Category with document count for filtering UI.
    """
    
    name: str = Field(..., description="Category display name")
    slug: str = Field(..., description="Category slug")
    description: Optional[str] = Field(default=None, description="Category description")
    document_count: int = Field(default=0, ge=0, description="Number of documents")
    icon: Optional[str] = Field(default=None, description="Optional icon identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "CRT Operations",
                "slug": "crt",
                "description": "Crisis Response Team operational guides",
                "document_count": 5,
                "icon": "shield",
            }
        }


class WikiTag(BaseModel):
    """
    Tag with document count for filtering UI.
    """
    
    name: str = Field(..., description="Tag name")
    document_count: int = Field(default=0, ge=0, description="Number of documents with this tag")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "crisis",
                "document_count": 8,
            }
        }


# =============================================================================
# Response Models (for API)
# =============================================================================


class WikiDocumentListResponse(BaseModel):
    """
    Response for document listing endpoint.
    """
    
    documents: List[WikiDocumentSummary] = Field(default_factory=list)
    total: int = Field(default=0, ge=0)
    category_filter: Optional[str] = Field(default=None)
    tag_filter: Optional[str] = Field(default=None)


class WikiSearchResponse(BaseModel):
    """
    Response for search endpoint.
    """
    
    query: str = Field(..., description="Original search query")
    results: List[WikiSearchResult] = Field(default_factory=list)
    total: int = Field(default=0, ge=0)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
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
