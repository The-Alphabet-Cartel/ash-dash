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
Wiki API Routes - Documentation wiki REST API endpoints
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.4-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET  /api/wiki/documents           - List all documents
    GET  /api/wiki/documents/{slug}    - Get document by slug
    GET  /api/wiki/documents/{slug}/pdf - Download document as PDF
    GET  /api/wiki/navigation          - Get navigation structure
    GET  /api/wiki/search              - Search documents
    GET  /api/wiki/categories          - List categories
    GET  /api/wiki/tags                - List tags
    GET  /api/wiki/styles              - Get CSS styles
"""

from io import BytesIO
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse, Response

from src.managers.wiki import (
    WikiManager,
    create_wiki_manager,
    WikiDocument,
    WikiDocumentSummary,
    WikiSearchResult,
    WikiNavigation,
    WikiCategory,
    WikiTag,
    WikiDocumentListResponse,
    WikiSearchResponse,
    get_wiki_styles,
    get_pygments_styles,
)

# Module version
__version__ = "v5.0-7-7.4-1"

# Create router
router = APIRouter(prefix="/api/wiki", tags=["Wiki"])


# =============================================================================
# Dependency Injection
# =============================================================================


def get_wiki_manager(request: Request) -> WikiManager:
    """
    Get WikiManager instance from application state.
    
    Creates a new instance if not already initialized.
    """
    # Check if wiki manager exists in app state
    if not hasattr(request.app.state, "wiki_manager") or request.app.state.wiki_manager is None:
        # Create wiki manager with config and logging from app state
        config_manager = getattr(request.app.state, "config_manager", None)
        logging_manager = getattr(request.app.state, "logging_manager", None)
        
        request.app.state.wiki_manager = create_wiki_manager(
            config_manager=config_manager,
            logging_manager=logging_manager,
        )
    
    return request.app.state.wiki_manager


# =============================================================================
# Document Endpoints
# =============================================================================


@router.get(
    "/documents",
    response_model=WikiDocumentListResponse,
    summary="List wiki documents",
    description="Get a list of all wiki documents with optional category and tag filtering.",
)
async def list_documents(
    category: Optional[str] = Query(
        None,
        description="Filter by category name (e.g., 'CRT Operations')",
    ),
    tag: Optional[str] = Query(
        None,
        description="Filter by tag (e.g., 'crisis')",
    ),
    wiki: WikiManager = Depends(get_wiki_manager),
) -> WikiDocumentListResponse:
    """
    List all wiki documents with optional filtering.
    
    Returns document summaries (without full content) for efficient loading.
    """
    documents = wiki.list_documents(category=category, tag=tag)
    
    return WikiDocumentListResponse(
        documents=documents,
        total=len(documents),
        category_filter=category,
        tag_filter=tag,
    )


@router.get(
    "/documents/{slug:path}",
    response_model=WikiDocument,
    summary="Get document by slug",
    description="Get a specific wiki document by its slug path.",
    responses={
        404: {"description": "Document not found"},
    },
)
async def get_document(
    slug: str,
    render: bool = Query(
        True,
        description="Whether to render Markdown to HTML",
    ),
    wiki: WikiManager = Depends(get_wiki_manager),
) -> WikiDocument:
    """
    Get a specific wiki document by slug.
    
    The slug is the path relative to the docs directory, without .md extension.
    Example: "crt/crisis-response-guide"
    
    If render=True (default), the content_html field will be populated
    with rendered HTML. If render=False, only content_md is returned.
    """
    if render:
        doc = wiki.get_rendered_document(slug)
    else:
        doc = wiki.get_document(slug)
    
    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {slug}",
        )
    
    return doc


@router.get(
    "/documents/{slug:path}/pdf",
    summary="Download document as PDF",
    description="Generate and download a PDF version of the document.",
    responses={
        404: {"description": "Document not found"},
        503: {"description": "PDF generation not available"},
    },
)
async def download_pdf(
    slug: str,
    wiki: WikiManager = Depends(get_wiki_manager),
) -> StreamingResponse:
    """
    Download a wiki document as a PDF file.
    
    The PDF includes Ash-Dash branding, headers, footers with page numbers,
    and print-optimized styling.
    """
    # Check if PDF generation is available
    if not wiki.is_pdf_available():
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint may not be installed.",
        )
    
    # Get document to check it exists
    doc = wiki.get_document(slug)
    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {slug}",
        )
    
    try:
        # Generate PDF
        pdf_bytes = wiki.generate_pdf(slug)
        
        # Generate filename from slug
        filename = slug.split("/")[-1] + ".pdf"
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}",
        )


# =============================================================================
# Navigation Endpoint
# =============================================================================


@router.get(
    "/navigation",
    response_model=WikiNavigation,
    summary="Get navigation structure",
    description="Get the navigation tree grouped by category for sidebar display.",
)
async def get_navigation(
    wiki: WikiManager = Depends(get_wiki_manager),
) -> WikiNavigation:
    """
    Get the wiki navigation structure.
    
    Returns categories with their documents, sorted appropriately for
    sidebar navigation. Includes category icons and document counts.
    """
    return wiki.get_navigation()


# =============================================================================
# Search Endpoint
# =============================================================================


@router.get(
    "/search",
    response_model=WikiSearchResponse,
    summary="Search documents",
    description="Full-text search across all wiki documents.",
)
async def search_documents(
    q: str = Query(
        ...,
        min_length=1,
        max_length=200,
        description="Search query string",
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    ),
    wiki: WikiManager = Depends(get_wiki_manager),
) -> WikiSearchResponse:
    """
    Search wiki documents by query.
    
    Searches across titles, tags, descriptions, and content with
    weighted scoring:
    - Title match: 10 points
    - Tag match: 5 points
    - Description match: 3 points
    - Content match: 1 point + occurrences
    
    Results include snippets with highlighted matches.
    """
    results = wiki.search(q, limit=limit)
    
    return WikiSearchResponse(
        query=q,
        results=results,
        total=len(results),
    )


# =============================================================================
# Category & Tag Endpoints
# =============================================================================


@router.get(
    "/categories",
    response_model=List[WikiCategory],
    summary="List categories",
    description="Get all categories with document counts.",
)
async def list_categories(
    wiki: WikiManager = Depends(get_wiki_manager),
) -> List[WikiCategory]:
    """
    Get all wiki categories with document counts.
    
    Includes category metadata like icon and description.
    Useful for building filter UI.
    """
    return wiki.get_categories()


@router.get(
    "/tags",
    response_model=List[WikiTag],
    summary="List tags",
    description="Get all tags with document counts.",
)
async def list_tags(
    wiki: WikiManager = Depends(get_wiki_manager),
) -> List[WikiTag]:
    """
    Get all wiki tags with document counts.
    
    Sorted by document count (descending), useful for tag clouds
    or filter UI.
    """
    return wiki.get_tags()


# =============================================================================
# Styles Endpoint
# =============================================================================


@router.get(
    "/styles",
    summary="Get wiki CSS styles",
    description="Get CSS styles for rendering wiki content.",
    response_class=Response,
)
async def get_styles(
    include_syntax: bool = Query(
        True,
        description="Include syntax highlighting CSS",
    ),
) -> Response:
    """
    Get CSS styles for wiki content rendering.
    
    Returns CSS that should be applied to wiki content for proper
    styling of prose, tables, code blocks, etc.
    
    If include_syntax=True (default), also includes Pygments CSS
    for syntax highlighting.
    """
    css = get_wiki_styles()
    
    if include_syntax:
        css += "\n\n/* Syntax Highlighting */\n"
        css += get_pygments_styles("monokai")
    
    return Response(
        content=css,
        media_type="text/css",
        headers={
            "Cache-Control": "public, max-age=86400",  # Cache for 24 hours
        },
    )


# =============================================================================
# Utility Endpoints
# =============================================================================


@router.post(
    "/refresh",
    summary="Refresh wiki cache",
    description="Force refresh of the wiki document cache.",
)
async def refresh_cache(
    wiki: WikiManager = Depends(get_wiki_manager),
) -> dict:
    """
    Force refresh of the wiki cache.
    
    Use this after adding or modifying wiki documents to ensure
    the latest content is served.
    """
    wiki.invalidate_cache()
    documents = wiki.scan_documents(force_refresh=True)
    
    return {
        "status": "refreshed",
        "documents_found": len(documents),
    }


@router.get(
    "/status",
    summary="Get wiki status",
    description="Get wiki system status and statistics.",
)
async def get_status(
    wiki: WikiManager = Depends(get_wiki_manager),
) -> dict:
    """
    Get wiki system status.
    
    Returns information about the wiki manager including
    document count, PDF availability, and docs path.
    """
    return {
        "status": "operational",
        "docs_path": str(wiki.docs_path),
        "document_count": wiki.document_count,
        "pdf_available": wiki.is_pdf_available(),
        "categories": len(wiki.get_categories()),
        "tags": len(wiki.get_tags()),
    }
