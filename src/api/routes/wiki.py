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
Wiki API Routes - Documentation wiki REST API endpoints with authorization
----------------------------------------------------------------------------
FILE VERSION: v5.0-11-11.11-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET  /api/wiki/documents           - List all documents (filtered by role)
    GET  /api/wiki/documents/{slug}    - Get document by slug (role-checked)
    GET  /api/wiki/pdf/{slug}          - Download document as PDF (role-checked)
    GET  /api/wiki/navigation          - Get navigation structure (filtered by role)
    GET  /api/wiki/search              - Search documents (filtered by role)
    GET  /api/wiki/categories          - List categories (filtered by role)
    GET  /api/wiki/tags                - List tags
    GET  /api/wiki/styles              - Get CSS styles

AUTHORIZATION (Phase 11):
    - All endpoints require CRT membership
    - Admin/Operations categories: Admin role required
    - Non-admin users cannot see or access restricted documents
"""

import logging
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

# Phase 11: Import auth dependencies
from src.api.dependencies.auth import require_member
from src.api.middleware.auth_middleware import UserContext

# Module version
__version__ = "v5.0-11-11.11-1"

# Initialize module logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/wiki", tags=["Wiki"])


# =============================================================================
# Category Access Control
# =============================================================================

# Categories restricted to Admin users only
# These contain backend server information, deployment details, etc.
ADMIN_ONLY_CATEGORIES = frozenset({
    "admin",
    "operations",
    "Administration",
    "Operations",
})

# Directory prefixes that map to admin-only categories
ADMIN_ONLY_PREFIXES = frozenset({
    "admin/",
    "operations/",
})


def is_admin_only_category(category: Optional[str]) -> bool:
    """Check if a category is restricted to admin users."""
    if not category:
        return False
    return category.lower() in {c.lower() for c in ADMIN_ONLY_CATEGORIES}


def is_admin_only_slug(slug: str) -> bool:
    """Check if a document slug is in an admin-only directory."""
    slug_lower = slug.lower()
    return any(slug_lower.startswith(prefix) for prefix in ADMIN_ONLY_PREFIXES)


def check_document_access(slug: str, user: UserContext) -> None:
    """
    Check if user has access to a document based on its path.
    
    Raises HTTPException 403 if access denied.
    """
    if is_admin_only_slug(slug) and not user.is_admin:
        logger.warning(
            f"Access denied to admin-only document: {slug} "
            f"(user: {user.email}, role: {user.role})"
        )
        raise HTTPException(
            status_code=403,
            detail="Access denied: Admin role required for this documentation",
        )


def filter_documents_by_role(
    documents: List[WikiDocumentSummary],
    user: UserContext,
) -> List[WikiDocumentSummary]:
    """Filter document list to only include documents the user can access."""
    if user.is_admin:
        return documents
    
    return [
        doc for doc in documents
        if not is_admin_only_category(doc.category) and not is_admin_only_slug(doc.slug)
    ]


def filter_categories_by_role(
    categories: List[WikiCategory],
    user: UserContext,
) -> List[WikiCategory]:
    """Filter category list to only include categories the user can access."""
    if user.is_admin:
        return categories
    
    return [
        cat for cat in categories
        if not is_admin_only_category(cat.name)
    ]


def filter_search_results_by_role(
    results: List[WikiSearchResult],
    user: UserContext,
) -> List[WikiSearchResult]:
    """Filter search results to only include documents the user can access."""
    if user.is_admin:
        return results
    
    return [
        result for result in results
        if not is_admin_only_category(result.category) and not is_admin_only_slug(result.slug)
    ]


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
    description="Get a list of all wiki documents with optional category and tag filtering. "
                "Admin and Operations categories are only visible to Admin users.",
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
    user: UserContext = Depends(require_member),
) -> WikiDocumentListResponse:
    """
    List all wiki documents with optional filtering.
    
    Returns document summaries (without full content) for efficient loading.
    Admin and Operations categories are filtered out for non-admin users.
    """
    # Check if requesting an admin-only category without admin role
    if category and is_admin_only_category(category) and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Admin role required for this category",
        )
    
    documents = wiki.list_documents(category=category, tag=tag)
    
    # Filter documents based on user role
    filtered_docs = filter_documents_by_role(documents, user)
    
    return WikiDocumentListResponse(
        documents=filtered_docs,
        total=len(filtered_docs),
        category_filter=category,
        tag_filter=tag,
    )


@router.get(
    "/documents/{slug:path}",
    response_model=WikiDocument,
    summary="Get document by slug",
    description="Get a specific wiki document by its slug path. "
                "Admin and Operations documents require Admin role.",
    responses={
        403: {"description": "Access denied - Admin role required"},
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
    user: UserContext = Depends(require_member),
) -> WikiDocument:
    """
    Get a specific wiki document by slug.
    
    The slug is the path relative to the docs directory, without .md extension.
    Example: "crt/crisis-response-guide"
    
    If render=True (default), the content_html field will be populated
    with rendered HTML. If render=False, only content_md is returned.
    
    Documents in admin/ or operations/ directories require Admin role.
    """
    # Check access before retrieving document
    check_document_access(slug, user)
    
    if render:
        doc = wiki.get_rendered_document(slug)
    else:
        doc = wiki.get_document(slug)
    
    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {slug}",
        )
    
    # Double-check category access (in case slug didn't match pattern)
    if is_admin_only_category(doc.category) and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Admin role required for this documentation",
        )
    
    return doc


@router.get(
    "/pdf/{slug:path}",
    summary="Download document as PDF",
    description="Generate and download a PDF version of the document. "
                "Admin and Operations documents require Admin role.",
    responses={
        403: {"description": "Access denied - Admin role required"},
        404: {"description": "Document not found"},
        503: {"description": "PDF generation not available"},
    },
)
async def download_pdf(
    slug: str,
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> StreamingResponse:
    """
    Download a wiki document as a PDF file.
    
    The PDF includes Ash-Dash branding, headers, footers with page numbers,
    and print-optimized styling.
    
    Documents in admin/ or operations/ directories require Admin role.
    """
    logger.info(f"📄 PDF download requested for: {slug} (user: {user.email})")
    
    # Check access before generating PDF
    check_document_access(slug, user)
    
    # Check if PDF generation is available
    if not wiki.is_pdf_available():
        logger.error("❌ PDF generation unavailable - WeasyPrint not installed")
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint may not be installed.",
        )
    
    # Get document to check it exists
    doc = wiki.get_document(slug)
    if not doc:
        logger.warning(f"⚠️ PDF request for non-existent document: {slug}")
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {slug}",
        )
    
    # Double-check category access
    if is_admin_only_category(doc.category) and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Admin role required for this documentation",
        )
    
    try:
        logger.info(f"📄 Generating PDF for: {doc.title}")
        
        # Generate PDF
        pdf_bytes = wiki.generate_pdf(slug)
        
        # Generate filename from slug
        filename = slug.split("/")[-1] + ".pdf"
        
        logger.info(f"✅ PDF generated: {filename} ({len(pdf_bytes):,} bytes)")
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )
        
    except Exception as e:
        # Log the full exception with traceback
        logger.error(f"❌ PDF generation failed for {slug}: {e}", exc_info=True)
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
    description="Get the navigation tree grouped by category for sidebar display. "
                "Admin and Operations categories are only visible to Admin users.",
)
async def get_navigation(
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> WikiNavigation:
    """
    Get the wiki navigation structure.
    
    Returns categories with their documents, sorted appropriately for
    sidebar navigation. Includes category icons and document counts.
    
    Admin and Operations categories are filtered out for non-admin users.
    """
    navigation = wiki.get_navigation()
    
    # Filter categories based on user role
    if not user.is_admin:
        navigation.categories = [
            cat for cat in navigation.categories
            if not is_admin_only_category(cat.name)
        ]
        # Recalculate total after filtering
        navigation.total_documents = sum(
            len(cat.documents) for cat in navigation.categories
        )
    
    return navigation


# =============================================================================
# Search Endpoint
# =============================================================================


@router.get(
    "/search",
    response_model=WikiSearchResponse,
    summary="Search documents",
    description="Full-text search across all wiki documents. "
                "Admin and Operations documents are excluded for non-admin users.",
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
    user: UserContext = Depends(require_member),
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
    Admin and Operations documents are filtered out for non-admin users.
    """
    results = wiki.search(q, limit=limit)
    
    # Filter results based on user role
    filtered_results = filter_search_results_by_role(results, user)
    
    return WikiSearchResponse(
        query=q,
        results=filtered_results,
        total=len(filtered_results),
    )


# =============================================================================
# Category & Tag Endpoints
# =============================================================================


@router.get(
    "/categories",
    response_model=List[WikiCategory],
    summary="List categories",
    description="Get all categories with document counts. "
                "Admin and Operations categories are only visible to Admin users.",
)
async def list_categories(
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> List[WikiCategory]:
    """
    Get all wiki categories with document counts.
    
    Includes category metadata like icon and description.
    Useful for building filter UI.
    
    Admin and Operations categories are filtered out for non-admin users.
    """
    categories = wiki.get_categories()
    
    # Filter categories based on user role
    filtered_categories = filter_categories_by_role(categories, user)
    
    return filtered_categories


@router.get(
    "/tags",
    response_model=List[WikiTag],
    summary="List tags",
    description="Get all tags with document counts.",
)
async def list_tags(
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> List[WikiTag]:
    """
    Get all wiki tags with document counts.
    
    Sorted by document count (descending), useful for tag clouds
    or filter UI.
    
    Note: Tags are not filtered by role. A tag may exist in both
    restricted and unrestricted documents.
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
    user: UserContext = Depends(require_member),
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
    description="Force refresh of the wiki document cache. Admin only.",
)
async def refresh_cache(
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> dict:
    """
    Force refresh of the wiki cache.
    
    Use this after adding or modifying wiki documents to ensure
    the latest content is served.
    
    Note: Any authenticated CRT member can refresh the cache.
    """
    wiki.invalidate_cache()
    documents = wiki.scan_documents(force_refresh=True)
    
    # Count visible documents for this user
    visible_count = len([
        d for d in documents
        if user.is_admin or not is_admin_only_slug(d.slug)
    ])
    
    logger.info(f"📚 Wiki cache refreshed by {user.email}: {len(documents)} total, {visible_count} visible to user")
    
    return {
        "status": "refreshed",
        "documents_found": visible_count,
    }


@router.get(
    "/status",
    summary="Get wiki status",
    description="Get wiki system status and statistics.",
)
async def get_status(
    wiki: WikiManager = Depends(get_wiki_manager),
    user: UserContext = Depends(require_member),
) -> dict:
    """
    Get wiki system status.
    
    Returns information about the wiki manager including
    document count, PDF availability, and docs path.
    
    Document count reflects only documents visible to the current user.
    """
    # Get categories visible to user
    all_categories = wiki.get_categories()
    visible_categories = filter_categories_by_role(all_categories, user)
    
    # Calculate visible document count
    visible_doc_count = sum(cat.document_count for cat in visible_categories)
    
    return {
        "status": "operational",
        "docs_path": str(wiki.docs_path),
        "document_count": visible_doc_count,
        "pdf_available": wiki.is_pdf_available(),
        "categories": len(visible_categories),
        "tags": len(wiki.get_tags()),
    }
