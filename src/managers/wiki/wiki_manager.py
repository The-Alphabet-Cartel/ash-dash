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
Wiki Manager - Documentation wiki management system
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.3-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Scan docs/ directory for Markdown files
- Parse frontmatter metadata (YAML)
- Cache parsed documents for performance
- Generate navigation structure from directory layout
- Provide search functionality across documents
- Render Markdown to styled HTML
- Generate PDF exports via WeasyPrint

USAGE:
    from src.managers.wiki import create_wiki_manager
    
    wiki = create_wiki_manager(config_manager, logging_manager)
    
    # Get all documents
    docs = wiki.scan_documents()
    
    # Get specific document
    doc = wiki.get_document("crt/crisis-response-guide")
    
    # Search documents
    results = wiki.search("crisis response")
    
    # Get navigation
    nav = wiki.get_navigation()
"""

import os
import re
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .models import (
    WikiDocument,
    WikiDocumentSummary,
    WikiTocEntry,
    WikiSearchResult,
    WikiNavItem,
    WikiNavCategory,
    WikiNavigation,
    WikiCategory,
    WikiTag,
)

# Module version
__version__ = "v5.0-7-7.3-1"

# Initialize fallback logger
logger = logging.getLogger(__name__)


# =============================================================================
# Category Configuration
# =============================================================================

# Category display names and icons (maps directory name -> display info)
CATEGORY_CONFIG: Dict[str, Dict[str, str]] = {
    "admin": {
        "name": "Administration",
        "icon": "settings",
        "description": "System administration and configuration guides",
    },
    "crt": {
        "name": "CRT Operations",
        "icon": "shield",
        "description": "Crisis Response Team procedures and protocols",
    },
    "reference": {
        "name": "Reference",
        "icon": "book-open",
        "description": "Technical reference materials and API documentation",
    },
    "training": {
        "name": "Training",
        "icon": "graduation-cap",
        "description": "Onboarding and training materials",
    },
    "general": {
        "name": "General",
        "icon": "file-text",
        "description": "General documentation",
    },
}

# Directories to exclude from wiki scanning
EXCLUDED_DIRS: Set[str] = {
    "v5.0",           # Development phases
    "standards",      # Internal standards
    "api",            # Internal API reference
    ".obsidian",      # Obsidian config
    ".git",           # Git directory
    "__pycache__",    # Python cache
}


class WikiManager:
    """
    Wiki Manager for documentation system.
    
    Implements Clean Architecture v5.2 principles:
    - Factory function pattern (create_wiki_manager)
    - Dependency injection (config_manager, logging_manager)
    - Resilient error handling with graceful fallbacks
    - Comprehensive logging for debugging
    
    Attributes:
        docs_path: Path to documentation directory
        cache: Dictionary of cached WikiDocument objects
        cache_valid: Whether cache is up-to-date
    """
    
    def __init__(
        self,
        config_manager: Any,
        logging_manager: Optional[Any] = None,
        docs_path: Optional[str] = None,
    ):
        """
        Initialize WikiManager.
        
        Args:
            config_manager: Configuration manager instance
            logging_manager: Optional logging manager for consistent logging
            docs_path: Optional custom docs directory path
            
        Note:
            Use create_wiki_manager() factory function instead of direct instantiation.
        """
        self._config = config_manager
        
        # Set up logging
        if logging_manager:
            self._logger = logging_manager.get_logger("wiki")
        else:
            self._logger = logger
        
        # Set docs path
        if docs_path:
            self._docs_path = Path(docs_path)
        else:
            # Default to docs/ in project root
            self._docs_path = Path(__file__).parent.parent.parent.parent / "docs"
        
        # Document cache
        self._cache: Dict[str, WikiDocument] = {}
        self._cache_time: Optional[datetime] = None
        self._cache_hash: Optional[str] = None
        
        # Navigation cache
        self._nav_cache: Optional[WikiNavigation] = None
        
        self._logger.info(
            f"✅ WikiManager v{__version__} initialized "
            f"(docs_path: {self._docs_path})"
        )
    
    # =========================================================================
    # Document Scanning
    # =========================================================================
    
    def scan_documents(self, force_refresh: bool = False) -> List[WikiDocument]:
        """
        Scan docs directory for Markdown files and parse them.
        
        Args:
            force_refresh: Force cache refresh even if valid
            
        Returns:
            List of WikiDocument objects
        """
        # Check cache validity
        if not force_refresh and self._is_cache_valid():
            self._logger.debug("Using cached documents")
            return list(self._cache.values())
        
        self._logger.info(f"📂 Scanning documents in: {self._docs_path}")
        
        documents: List[WikiDocument] = []
        
        if not self._docs_path.exists():
            self._logger.warning(f"⚠️ Docs directory not found: {self._docs_path}")
            return documents
        
        for root, dirs, files in os.walk(self._docs_path):
            # Remove excluded directories from walk
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            # Determine category from directory structure
            rel_root = Path(root).relative_to(self._docs_path)
            category_slug = str(rel_root).split(os.sep)[0] if str(rel_root) != "." else "general"
            
            for filename in files:
                # Only process Markdown files, skip hidden files
                if not filename.endswith(".md") or filename.startswith("."):
                    continue
                
                file_path = Path(root) / filename
                doc = self._parse_document(file_path, category_slug)
                
                if doc:
                    documents.append(doc)
                    self._cache[doc.slug] = doc
        
        # Update cache metadata
        self._cache_time = datetime.now()
        self._cache_hash = self._compute_docs_hash()
        self._nav_cache = None  # Invalidate navigation cache
        
        self._logger.info(f"✅ Scanned {len(documents)} documents")
        
        return documents
    
    def _parse_document(
        self,
        file_path: Path,
        default_category: str,
    ) -> Optional[WikiDocument]:
        """
        Parse a Markdown file with frontmatter.
        
        Args:
            file_path: Path to the Markdown file
            default_category: Default category from directory
            
        Returns:
            WikiDocument or None on error
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract frontmatter
            frontmatter: Dict[str, Any] = {}
            body = content
            
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError as e:
                        self._logger.warning(
                            f"⚠️ Invalid YAML frontmatter in {file_path}: {e}"
                        )
                    body = parts[2].strip()
            
            # Generate slug from path
            slug = str(file_path.relative_to(self._docs_path))[:-3]  # Remove .md
            slug = slug.replace("\\", "/").replace(" ", "-").lower()
            
            # Get file modification time
            file_stat = file_path.stat()
            file_modified = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Extract table of contents from headings
            toc = self._extract_toc(body)
            
            # Determine category (frontmatter overrides directory)
            category = frontmatter.get("category", default_category)
            if category in CATEGORY_CONFIG:
                category = CATEGORY_CONFIG[category]["name"]
            
            return WikiDocument(
                slug=slug,
                file_path=str(file_path),
                title=frontmatter.get(
                    "title",
                    file_path.stem.replace("-", " ").replace("_", " ").title()
                ),
                description=frontmatter.get("description", ""),
                category=category,
                tags=frontmatter.get("tags", []),
                author=frontmatter.get("author", "Unknown"),
                version=str(frontmatter.get("version", "1.0")),
                last_updated=frontmatter.get("last_updated"),
                file_modified=file_modified,
                content_md=body,
                content_html=None,  # Rendered on demand
                toc=toc,
            )
            
        except Exception as e:
            self._logger.error(f"❌ Failed to parse {file_path}: {e}")
            return None
    
    def _extract_toc(self, content: str) -> List[WikiTocEntry]:
        """
        Extract table of contents from Markdown headings.
        
        Args:
            content: Markdown content
            
        Returns:
            List of WikiTocEntry objects
        """
        toc: List[WikiTocEntry] = []
        
        # Match Markdown headings (# Heading)
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        
        for match in heading_pattern.finditer(content):
            level = len(match.group(1))
            text = match.group(2).strip()
            
            # Generate anchor (lowercase, spaces to hyphens, remove special chars)
            anchor = re.sub(r"[^\w\s-]", "", text.lower())
            anchor = re.sub(r"[-\s]+", "-", anchor).strip("-")
            
            toc.append(WikiTocEntry(
                level=level,
                text=text,
                anchor=anchor,
            ))
        
        return toc
    
    # =========================================================================
    # Document Retrieval
    # =========================================================================
    
    def get_document(self, slug: str) -> Optional[WikiDocument]:
        """
        Get a document by its slug.
        
        Args:
            slug: Document slug (e.g., "crt/crisis-response-guide")
            
        Returns:
            WikiDocument or None if not found
        """
        # Ensure cache is populated
        if not self._cache:
            self.scan_documents()
        
        # Normalize slug
        slug = slug.lower().strip("/")
        
        return self._cache.get(slug)
    
    def get_rendered_document(
        self,
        slug: str,
        base_path: str = "/wiki",
    ) -> Optional[WikiDocument]:
        """
        Get a document with rendered HTML content.
        
        Args:
            slug: Document slug
            base_path: Base path for internal links
            
        Returns:
            WikiDocument with content_html populated, or None if not found
        """
        doc = self.get_document(slug)
        if not doc:
            return None
        
        # Render if not already rendered
        if not doc.content_html:
            doc = self.render_document(doc, base_path)
        
        return doc
    
    def render_document(
        self,
        doc: WikiDocument,
        base_path: str = "/wiki",
    ) -> WikiDocument:
        """
        Render a document's Markdown content to HTML.
        
        Args:
            doc: WikiDocument to render
            base_path: Base path for internal links
            
        Returns:
            WikiDocument with content_html populated
        """
        from .markdown_renderer import create_markdown_renderer
        
        try:
            renderer = create_markdown_renderer(base_path=base_path)
            html = renderer.render(doc.content_md)
            
            # Create new document with rendered HTML
            # (Pydantic models are immutable by default)
            return WikiDocument(
                slug=doc.slug,
                file_path=doc.file_path,
                title=doc.title,
                description=doc.description,
                category=doc.category,
                tags=doc.tags,
                author=doc.author,
                version=doc.version,
                last_updated=doc.last_updated,
                file_modified=doc.file_modified,
                content_md=doc.content_md,
                content_html=html,
                toc=doc.toc,
            )
            
        except Exception as e:
            self._logger.error(f"❌ Failed to render document {doc.slug}: {e}")
            # Return with escaped content as fallback
            escaped = (
                doc.content_md
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            return WikiDocument(
                slug=doc.slug,
                file_path=doc.file_path,
                title=doc.title,
                description=doc.description,
                category=doc.category,
                tags=doc.tags,
                author=doc.author,
                version=doc.version,
                last_updated=doc.last_updated,
                file_modified=doc.file_modified,
                content_md=doc.content_md,
                content_html=f"<pre>{escaped}</pre>",
                toc=doc.toc,
            )
    
    def get_document_summary(self, doc: WikiDocument) -> WikiDocumentSummary:
        """
        Convert WikiDocument to WikiDocumentSummary.
        
        Args:
            doc: Full WikiDocument
            
        Returns:
            WikiDocumentSummary without content
        """
        return WikiDocumentSummary(
            slug=doc.slug,
            title=doc.title,
            description=doc.description,
            category=doc.category,
            tags=doc.tags,
            author=doc.author,
            last_updated=doc.last_updated,
        )
    
    def list_documents(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[WikiDocumentSummary]:
        """
        List documents with optional filtering.
        
        Args:
            category: Filter by category name
            tag: Filter by tag
            
        Returns:
            List of WikiDocumentSummary objects
        """
        docs = self.scan_documents()
        
        # Apply filters
        if category:
            category_lower = category.lower()
            docs = [d for d in docs if d.category.lower() == category_lower]
        
        if tag:
            tag_lower = tag.lower()
            docs = [d for d in docs if tag_lower in [t.lower() for t in d.tags]]
        
        # Convert to summaries and sort by title
        summaries = [self.get_document_summary(d) for d in docs]
        summaries.sort(key=lambda x: x.title.lower())
        
        return summaries
    
    # =========================================================================
    # Navigation
    # =========================================================================
    
    def get_navigation(self) -> WikiNavigation:
        """
        Get navigation structure grouped by category.
        
        Returns:
            WikiNavigation with categories and documents
        """
        # Check cache
        if self._nav_cache and self._is_cache_valid():
            return self._nav_cache
        
        docs = self.scan_documents()
        
        # Group documents by category
        categories_map: Dict[str, List[WikiNavItem]] = {}
        
        for doc in docs:
            category = doc.category
            if category not in categories_map:
                categories_map[category] = []
            
            categories_map[category].append(WikiNavItem(
                slug=doc.slug,
                title=doc.title,
            ))
        
        # Build navigation categories
        categories: List[WikiNavCategory] = []
        
        for cat_name, items in sorted(categories_map.items()):
            # Find config for this category
            cat_slug = cat_name.lower().replace(" ", "-")
            cat_config = None
            
            for slug, config in CATEGORY_CONFIG.items():
                if config["name"] == cat_name or slug == cat_slug:
                    cat_config = config
                    cat_slug = slug
                    break
            
            # Sort documents by title
            items.sort(key=lambda x: x.title.lower())
            
            categories.append(WikiNavCategory(
                name=cat_name,
                slug=cat_slug,
                icon=cat_config["icon"] if cat_config else "file-text",
                documents=items,
            ))
        
        # Sort categories (put "General" last)
        categories.sort(key=lambda x: (x.name == "General", x.name.lower()))
        
        self._nav_cache = WikiNavigation(
            categories=categories,
            total_documents=len(docs),
        )
        
        return self._nav_cache
    
    # =========================================================================
    # Search
    # =========================================================================
    
    def search(self, query: str, limit: int = 20) -> List[WikiSearchResult]:
        """
        Search documents by query.
        
        Searches in order of weight:
        1. Title (weight: 10)
        2. Tags (weight: 5)
        3. Description (weight: 3)
        4. Content (weight: 1 + occurrence count)
        
        Args:
            query: Search query string
            limit: Maximum results to return
            
        Returns:
            List of WikiSearchResult sorted by score
        """
        if not query or not query.strip():
            return []
        
        docs = self.scan_documents()
        results: List[WikiSearchResult] = []
        query_lower = query.lower().strip()
        query_words = query_lower.split()
        
        for doc in docs:
            score = 0.0
            match_locations: List[str] = []
            
            # Title match (highest weight)
            title_lower = doc.title.lower()
            if query_lower in title_lower:
                score += 10
                match_locations.append("title")
            else:
                # Partial word matches in title
                for word in query_words:
                    if word in title_lower:
                        score += 3
                        if "title" not in match_locations:
                            match_locations.append("title")
            
            # Tag matches
            for tag in doc.tags:
                tag_lower = tag.lower()
                if query_lower in tag_lower or tag_lower in query_lower:
                    score += 5
                    if "tags" not in match_locations:
                        match_locations.append("tags")
            
            # Description match
            if query_lower in doc.description.lower():
                score += 3
                match_locations.append("description")
            
            # Content match
            content_lower = doc.content_md.lower()
            if query_lower in content_lower:
                score += 1
                # Bonus for multiple occurrences
                occurrences = content_lower.count(query_lower)
                score += min(occurrences * 0.5, 5)  # Cap at +5
                match_locations.append("content")
            
            if score > 0:
                results.append(WikiSearchResult(
                    document=self.get_document_summary(doc),
                    score=score,
                    snippet=self._extract_snippet(doc.content_md, query),
                    match_locations=match_locations,
                ))
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def _extract_snippet(
        self,
        content: str,
        query: str,
        context_chars: int = 100,
    ) -> str:
        """
        Extract a snippet around the first query match.
        
        Args:
            content: Full content to search
            query: Query to find
            context_chars: Characters of context on each side
            
        Returns:
            Snippet with match highlighted in **bold**
        """
        query_lower = query.lower()
        content_lower = content.lower()
        
        pos = content_lower.find(query_lower)
        if pos == -1:
            # No exact match, return beginning of content
            return content[:context_chars * 2].strip() + "..."
        
        # Calculate snippet bounds
        start = max(0, pos - context_chars)
        end = min(len(content), pos + len(query) + context_chars)
        
        # Extract snippet
        snippet = content[start:end]
        
        # Clean up - start at word boundary
        if start > 0:
            space_pos = snippet.find(" ")
            if space_pos > 0 and space_pos < 20:
                snippet = snippet[space_pos + 1:]
            snippet = "..." + snippet
        
        # Clean up - end at word boundary
        if end < len(content):
            space_pos = snippet.rfind(" ")
            if space_pos > len(snippet) - 20:
                snippet = snippet[:space_pos]
            snippet = snippet + "..."
        
        # Highlight match (case-insensitive replacement)
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        snippet = pattern.sub(f"**{query}**", snippet)
        
        return snippet.strip()
    
    # =========================================================================
    # Categories & Tags
    # =========================================================================
    
    def get_categories(self) -> List[WikiCategory]:
        """
        Get all categories with document counts.
        
        Returns:
            List of WikiCategory objects
        """
        docs = self.scan_documents()
        
        # Count documents per category
        category_counts: Dict[str, int] = {}
        for doc in docs:
            category_counts[doc.category] = category_counts.get(doc.category, 0) + 1
        
        categories: List[WikiCategory] = []
        for cat_name, count in sorted(category_counts.items()):
            # Find config for this category
            cat_slug = cat_name.lower().replace(" ", "-")
            cat_config = None
            
            for slug, config in CATEGORY_CONFIG.items():
                if config["name"] == cat_name or slug == cat_slug:
                    cat_config = config
                    cat_slug = slug
                    break
            
            categories.append(WikiCategory(
                name=cat_name,
                slug=cat_slug,
                description=cat_config["description"] if cat_config else None,
                document_count=count,
                icon=cat_config["icon"] if cat_config else "file-text",
            ))
        
        # Sort by name (General last)
        categories.sort(key=lambda x: (x.name == "General", x.name.lower()))
        
        return categories
    
    def get_tags(self) -> List[WikiTag]:
        """
        Get all tags with document counts.
        
        Returns:
            List of WikiTag objects sorted by count (descending)
        """
        docs = self.scan_documents()
        
        # Count documents per tag
        tag_counts: Dict[str, int] = {}
        for doc in docs:
            for tag in doc.tags:
                tag_lower = tag.lower()
                tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1
        
        tags = [
            WikiTag(name=tag, document_count=count)
            for tag, count in tag_counts.items()
        ]
        
        # Sort by count descending, then name ascending
        tags.sort(key=lambda x: (-x.document_count, x.name.lower()))
        
        return tags
    
    # =========================================================================
    # Cache Management
    # =========================================================================
    
    def _is_cache_valid(self) -> bool:
        """
        Check if document cache is still valid.
        
        Cache is invalid if:
        - Cache is empty
        - Docs directory hash changed
        
        Returns:
            True if cache is valid
        """
        if not self._cache or not self._cache_hash:
            return False
        
        current_hash = self._compute_docs_hash()
        return current_hash == self._cache_hash
    
    def _compute_docs_hash(self) -> str:
        """
        Compute hash of docs directory structure and file modification times.
        
        Returns:
            MD5 hash string
        """
        hash_input = []
        
        if not self._docs_path.exists():
            return ""
        
        for root, dirs, files in os.walk(self._docs_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for filename in sorted(files):
                if filename.endswith(".md") and not filename.startswith("."):
                    file_path = Path(root) / filename
                    try:
                        mtime = file_path.stat().st_mtime
                        hash_input.append(f"{file_path}:{mtime}")
                    except OSError:
                        pass
        
        return hashlib.md5("\n".join(hash_input).encode()).hexdigest()
    
    def invalidate_cache(self) -> None:
        """
        Manually invalidate the document cache.
        
        Call this when you know documents have changed.
        """
        self._cache.clear()
        self._cache_hash = None
        self._cache_time = None
        self._nav_cache = None
        self._logger.info("🔄 Wiki cache invalidated")
    
    # =========================================================================
    # PDF Generation
    # =========================================================================
    
    def generate_pdf(
        self,
        slug: str,
        base_path: str = "/wiki",
    ) -> bytes:
        """
        Generate a PDF for a wiki document.
        
        Args:
            slug: Document slug
            base_path: Base path for internal links
            
        Returns:
            PDF file as bytes
            
        Raises:
            ValueError: If document not found
            RuntimeError: If PDF generation fails
        """
        from .pdf_generator import create_pdf_generator
        
        # Get rendered document
        doc = self.get_rendered_document(slug, base_path)
        if not doc:
            raise ValueError(f"Document not found: {slug}")
        
        # Generate PDF
        generator = create_pdf_generator()
        
        if not generator.available:
            raise RuntimeError(
                "PDF generation not available. "
                "WeasyPrint may not be installed correctly."
            )
        
        return generator.generate(doc)
    
    def is_pdf_available(self) -> bool:
        """
        Check if PDF generation is available.
        
        Returns:
            True if WeasyPrint is installed and working
        """
        try:
            from .pdf_generator import create_pdf_generator
            generator = create_pdf_generator()
            return generator.available
        except Exception:
            return False
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    @property
    def docs_path(self) -> Path:
        """Get the documentation directory path."""
        return self._docs_path
    
    @property
    def document_count(self) -> int:
        """Get total number of cached documents."""
        return len(self._cache)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"WikiManager(docs_path='{self._docs_path}', "
            f"documents={len(self._cache)})"
        )


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2 Compliance (Rule #1)
# =============================================================================


def create_wiki_manager(
    config_manager: Any,
    logging_manager: Optional[Any] = None,
    docs_path: Optional[str] = None,
) -> WikiManager:
    """
    Factory function for WikiManager (Clean Architecture v5.2 Pattern).
    
    This is the ONLY way to create a WikiManager instance.
    Direct instantiation should be avoided in production code.
    
    Args:
        config_manager: Configuration manager instance
        logging_manager: Optional logging manager for consistent logging
        docs_path: Optional custom docs directory path
        
    Returns:
        Configured WikiManager instance
        
    Example:
        >>> wiki = create_wiki_manager(config_manager, logging_manager)
        >>> docs = wiki.scan_documents()
        >>> doc = wiki.get_document("crt/crisis-response-guide")
    """
    return WikiManager(
        config_manager=config_manager,
        logging_manager=logging_manager,
        docs_path=docs_path,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = ["WikiManager", "create_wiki_manager"]
