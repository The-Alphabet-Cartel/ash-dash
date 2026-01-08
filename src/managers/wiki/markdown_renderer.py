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
Markdown Renderer - Convert Markdown to styled HTML
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.2-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Convert Markdown to HTML
- Apply syntax highlighting to code blocks
- Generate table of contents with anchors
- Resolve internal wiki links
- Apply dark mode compatible styling

USAGE:
    from src.managers.wiki.markdown_renderer import create_markdown_renderer
    
    renderer = create_markdown_renderer()
    html = renderer.render(markdown_content)
    
    # With base path for internal links
    html = renderer.render(markdown_content, base_path="/wiki")
"""

import re
import logging
from typing import Any, Dict, List, Optional, Tuple

import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.preprocessors import Preprocessor
import xml.etree.ElementTree as etree

# Module version
__version__ = "v5.0-7-7.2-1"

# Initialize fallback logger
logger = logging.getLogger(__name__)


# =============================================================================
# Custom Extensions
# =============================================================================


class WikiLinkPreprocessor(Preprocessor):
    """
    Preprocessor to convert wiki-style links to standard Markdown links.
    
    Converts:
        [/crt/crisis-response-guide] -> [Crisis Response Guide](/wiki/crt/crisis-response-guide)
        [link text](/path) -> [link text](/wiki/path) (if internal)
    """
    
    def __init__(self, md: markdown.Markdown, base_path: str = "/wiki"):
        super().__init__(md)
        self.base_path = base_path.rstrip("/")
    
    def run(self, lines: List[str]) -> List[str]:
        """Process lines and convert wiki links."""
        new_lines = []
        
        # Pattern for wiki-style links: [/path/to/doc]
        wiki_pattern = re.compile(r'\[(/[^\]]+)\](?!\()')
        
        # Pattern for internal links: [text](/path)
        internal_pattern = re.compile(r'\[([^\]]+)\]\((/[^)]+)\)')
        
        for line in lines:
            # Convert wiki-style links [/path] to [Title](/wiki/path)
            def wiki_replace(match):
                path = match.group(1)
                # Generate title from path
                title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()
                return f"[{title}]({self.base_path}{path})"
            
            line = wiki_pattern.sub(wiki_replace, line)
            
            # Prepend base_path to internal links
            def internal_replace(match):
                text = match.group(1)
                path = match.group(2)
                # Don't modify external links or anchors
                if path.startswith("/wiki") or path.startswith("#"):
                    return match.group(0)
                return f"[{text}]({self.base_path}{path})"
            
            line = internal_pattern.sub(internal_replace, line)
            
            new_lines.append(line)
        
        return new_lines


class WikiLinkExtension(Extension):
    """Extension to handle wiki-style internal links."""
    
    def __init__(self, **kwargs):
        self.config = {
            "base_path": ["/wiki", "Base path for internal links"],
        }
        super().__init__(**kwargs)
    
    def extendMarkdown(self, md: markdown.Markdown) -> None:
        """Add the preprocessor to markdown."""
        base_path = self.getConfig("base_path")
        preprocessor = WikiLinkPreprocessor(md, base_path)
        md.preprocessors.register(preprocessor, "wiki_links", 25)


class HeadingAnchorTreeprocessor(Treeprocessor):
    """
    Treeprocessor to add anchor IDs to headings for TOC linking.
    """
    
    def __init__(self, md: markdown.Markdown):
        super().__init__(md)
        self.used_ids: Dict[str, int] = {}
    
    def run(self, root: etree.Element) -> etree.Element:
        """Process element tree and add IDs to headings."""
        self.used_ids.clear()
        
        for element in root.iter():
            if element.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                # Get heading text
                text = "".join(element.itertext())
                
                # Generate ID
                anchor_id = self._generate_id(text)
                
                # Set ID attribute
                element.set("id", anchor_id)
        
        return root
    
    def _generate_id(self, text: str) -> str:
        """Generate a unique anchor ID from heading text."""
        # Convert to lowercase
        anchor = text.lower()
        
        # Remove special characters, keep alphanumeric and spaces
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        
        # Replace spaces with hyphens
        anchor = re.sub(r"[-\s]+", "-", anchor).strip("-")
        
        # Ensure uniqueness
        base_anchor = anchor
        count = self.used_ids.get(base_anchor, 0)
        
        if count > 0:
            anchor = f"{base_anchor}-{count}"
        
        self.used_ids[base_anchor] = count + 1
        
        return anchor


class HeadingAnchorExtension(Extension):
    """Extension to add anchor IDs to headings."""
    
    def extendMarkdown(self, md: markdown.Markdown) -> None:
        """Add the treeprocessor to markdown."""
        treeprocessor = HeadingAnchorTreeprocessor(md)
        md.treeprocessors.register(treeprocessor, "heading_anchors", 15)


# =============================================================================
# Markdown Renderer Class
# =============================================================================


class MarkdownRenderer:
    """
    Markdown to HTML renderer with wiki-specific features.
    
    Features:
    - Syntax highlighting for code blocks (Pygments)
    - Tables support
    - Task lists (checkboxes)
    - Table of contents generation
    - Internal link handling
    - Dark mode compatible output
    
    Attributes:
        md: Configured Markdown instance
        base_path: Base path for internal wiki links
    """
    
    # Default Pygments style for code highlighting
    PYGMENTS_STYLE = "monokai"
    
    # CSS classes added to various elements
    CSS_CLASSES = {
        "table": "wiki-table",
        "code": "wiki-code",
        "blockquote": "wiki-blockquote",
    }
    
    def __init__(
        self,
        base_path: str = "/wiki",
        logging_manager: Optional[Any] = None,
    ):
        """
        Initialize MarkdownRenderer.
        
        Args:
            base_path: Base path for internal wiki links
            logging_manager: Optional logging manager
            
        Note:
            Use create_markdown_renderer() factory function.
        """
        self._base_path = base_path
        
        # Set up logging
        if logging_manager:
            self._logger = logging_manager.get_logger("markdown")
        else:
            self._logger = logger
        
        # Configure Markdown with extensions
        self._md = markdown.Markdown(
            extensions=[
                # Built-in extensions
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "attr_list",
                "def_list",
                "abbr",
                "md_in_html",
                "sane_lists",
                # Custom extensions
                WikiLinkExtension(base_path=base_path),
                HeadingAnchorExtension(),
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "guess_lang": True,
                    "linenums": False,
                    "pygments_style": self.PYGMENTS_STYLE,
                },
                "toc": {
                    "permalink": True,
                    "permalink_class": "toc-link",
                    "permalink_title": "Link to this section",
                    "toc_depth": "2-4",
                },
            },
        )
        
        self._logger.info(f"✅ MarkdownRenderer v{__version__} initialized")
    
    def render(
        self,
        content: str,
        base_path: Optional[str] = None,
    ) -> str:
        """
        Render Markdown content to HTML.
        
        Args:
            content: Markdown content string
            base_path: Override base path for this render
            
        Returns:
            Rendered HTML string
        """
        if not content:
            return ""
        
        # Reset markdown instance for fresh render
        self._md.reset()
        
        # Update base path if provided
        if base_path:
            for prep in self._md.preprocessors:
                if isinstance(self._md.preprocessors[prep], WikiLinkPreprocessor):
                    self._md.preprocessors[prep].base_path = base_path.rstrip("/")
        
        try:
            html = self._md.convert(content)
            
            # Post-process HTML for additional styling
            html = self._post_process(html)
            
            return html
            
        except Exception as e:
            self._logger.error(f"❌ Markdown render failed: {e}")
            # Return escaped content as fallback
            return f"<pre>{self._escape_html(content)}</pre>"
    
    def render_with_toc(
        self,
        content: str,
        base_path: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Render Markdown and return both HTML and TOC.
        
        Args:
            content: Markdown content string
            base_path: Override base path for this render
            
        Returns:
            Tuple of (rendered_html, toc_html)
        """
        html = self.render(content, base_path)
        
        # Get TOC from markdown instance
        toc_html = getattr(self._md, "toc", "")
        
        return html, toc_html
    
    def _post_process(self, html: str) -> str:
        """
        Post-process rendered HTML for additional styling.
        
        Args:
            html: Rendered HTML
            
        Returns:
            Post-processed HTML
        """
        # Add classes to tables
        html = html.replace(
            "<table>",
            f'<table class="{self.CSS_CLASSES["table"]}">'
        )
        
        # Add classes to blockquotes
        html = html.replace(
            "<blockquote>",
            f'<blockquote class="{self.CSS_CLASSES["blockquote"]}">'
        )
        
        # Add target="_blank" to external links
        html = re.sub(
            r'<a href="(https?://[^"]+)"',
            r'<a href="\1" target="_blank" rel="noopener noreferrer"',
            html
        )
        
        # Convert task list items
        html = self._convert_task_lists(html)
        
        return html
    
    def _convert_task_lists(self, html: str) -> str:
        """
        Convert GitHub-style task lists to proper HTML checkboxes.
        
        Converts:
            <li>[ ] Unchecked item</li>
            <li>[x] Checked item</li>
        
        To:
            <li class="task-item"><input type="checkbox" disabled> Unchecked item</li>
            <li class="task-item"><input type="checkbox" disabled checked> Checked item</li>
        """
        # Unchecked items
        html = re.sub(
            r'<li>\[ \](.+?)</li>',
            r'<li class="task-item"><input type="checkbox" disabled>\1</li>',
            html
        )
        
        # Checked items
        html = re.sub(
            r'<li>\[x\](.+?)</li>',
            r'<li class="task-item"><input type="checkbox" disabled checked>\1</li>',
            html,
            flags=re.IGNORECASE
        )
        
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
    
    def get_toc(self) -> str:
        """
        Get the table of contents from the last render.
        
        Returns:
            TOC HTML string
        """
        return getattr(self._md, "toc", "")
    
    def get_toc_tokens(self) -> List[Dict[str, Any]]:
        """
        Get the table of contents as structured tokens.
        
        Returns:
            List of TOC token dictionaries
        """
        return getattr(self._md, "toc_tokens", [])
    
    @property
    def base_path(self) -> str:
        """Get the base path for internal links."""
        return self._base_path
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"MarkdownRenderer(base_path='{self._base_path}')"


# =============================================================================
# CSS Styles for Rendered Content
# =============================================================================


def get_wiki_styles() -> str:
    """
    Get CSS styles for wiki content.
    
    These styles are designed to work with both light and dark modes.
    They should be included in the page that displays wiki content.
    
    Returns:
        CSS string for wiki styling
    """
    return """
/* ==========================================================================
   Wiki Content Styles - Ash-Dash v5.0
   Dark mode compatible
   ========================================================================== */

/* Base prose styling */
.wiki-content {
    line-height: 1.7;
    color: inherit;
}

.wiki-content > *:first-child {
    margin-top: 0;
}

/* Headings */
.wiki-content h1,
.wiki-content h2,
.wiki-content h3,
.wiki-content h4,
.wiki-content h5,
.wiki-content h6 {
    font-weight: 600;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    scroll-margin-top: 80px; /* Account for fixed header */
}

.wiki-content h1 { font-size: 2em; }
.wiki-content h2 { font-size: 1.5em; border-bottom: 1px solid rgba(128, 128, 128, 0.3); padding-bottom: 0.3em; }
.wiki-content h3 { font-size: 1.25em; }
.wiki-content h4 { font-size: 1.1em; }

/* Permalink anchors */
.wiki-content .toc-link {
    opacity: 0;
    margin-left: 0.5em;
    text-decoration: none;
    color: #9333EA;
    transition: opacity 0.2s;
}

.wiki-content h1:hover .toc-link,
.wiki-content h2:hover .toc-link,
.wiki-content h3:hover .toc-link,
.wiki-content h4:hover .toc-link {
    opacity: 1;
}

/* Paragraphs */
.wiki-content p {
    margin-top: 1em;
    margin-bottom: 1em;
}

/* Links */
.wiki-content a {
    color: #A855F7;
    text-decoration: none;
}

.wiki-content a:hover {
    text-decoration: underline;
}

/* External link indicator */
.wiki-content a[target="_blank"]::after {
    content: " ↗";
    font-size: 0.75em;
    opacity: 0.7;
}

/* Lists */
.wiki-content ul,
.wiki-content ol {
    margin: 1em 0;
    padding-left: 2em;
}

.wiki-content li {
    margin: 0.25em 0;
}

.wiki-content li > p {
    margin: 0.25em 0;
}

/* Task lists */
.wiki-content .task-item {
    list-style: none;
    margin-left: -1.5em;
}

.wiki-content .task-item input[type="checkbox"] {
    margin-right: 0.5em;
    accent-color: #9333EA;
}

/* Tables */
.wiki-content .wiki-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    font-size: 0.95em;
}

.wiki-content .wiki-table th,
.wiki-content .wiki-table td {
    padding: 0.75em 1em;
    text-align: left;
    border: 1px solid rgba(128, 128, 128, 0.3);
}

.wiki-content .wiki-table th {
    background: rgba(147, 51, 234, 0.1);
    font-weight: 600;
}

.wiki-content .wiki-table tr:nth-child(even) {
    background: rgba(128, 128, 128, 0.05);
}

/* Code - Inline */
.wiki-content code {
    background: rgba(128, 128, 128, 0.15);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
    font-size: 0.9em;
}

/* Code - Blocks (with syntax highlighting) */
.wiki-content .highlight {
    background: #1f2937;
    border-radius: 8px;
    padding: 1em;
    overflow-x: auto;
    margin: 1.5em 0;
}

.wiki-content .highlight pre {
    margin: 0;
    padding: 0;
    background: transparent;
}

.wiki-content .highlight code {
    background: transparent;
    padding: 0;
    font-size: 0.9em;
    line-height: 1.5;
}

/* Blockquotes */
.wiki-content .wiki-blockquote {
    border-left: 4px solid #9333EA;
    margin: 1.5em 0;
    padding: 0.5em 1em;
    background: rgba(147, 51, 234, 0.05);
    font-style: italic;
}

.wiki-content .wiki-blockquote p {
    margin: 0.5em 0;
}

/* Horizontal rules */
.wiki-content hr {
    border: none;
    border-top: 1px solid rgba(128, 128, 128, 0.3);
    margin: 2em 0;
}

/* Images */
.wiki-content img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1em 0;
}

/* Definition lists */
.wiki-content dl {
    margin: 1em 0;
}

.wiki-content dt {
    font-weight: 600;
    margin-top: 1em;
}

.wiki-content dd {
    margin-left: 2em;
    margin-top: 0.25em;
}

/* Table of Contents (sidebar) */
.wiki-toc {
    font-size: 0.9em;
}

.wiki-toc ul {
    list-style: none;
    padding-left: 1em;
    margin: 0;
}

.wiki-toc > ul {
    padding-left: 0;
}

.wiki-toc li {
    margin: 0.5em 0;
}

.wiki-toc a {
    color: inherit;
    text-decoration: none;
    opacity: 0.8;
    transition: opacity 0.2s, color 0.2s;
}

.wiki-toc a:hover {
    opacity: 1;
    color: #A855F7;
}

/* Emoji support */
.wiki-content .emoji {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
}

/* Print styles */
@media print {
    .wiki-content .toc-link {
        display: none;
    }
    
    .wiki-content a[target="_blank"]::after {
        content: " (" attr(href) ")";
    }
    
    .wiki-content .highlight {
        background: #f5f5f5 !important;
        border: 1px solid #ddd;
    }
}
"""


# =============================================================================
# Pygments CSS for Syntax Highlighting
# =============================================================================


def get_pygments_styles(style: str = "monokai") -> str:
    """
    Get Pygments CSS for syntax highlighting.
    
    Args:
        style: Pygments style name (default: monokai for dark mode)
        
    Returns:
        CSS string for syntax highlighting
    """
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.styles import get_style_by_name
        
        formatter = HtmlFormatter(style=style)
        return formatter.get_style_defs(".highlight")
        
    except ImportError:
        logger.warning("Pygments not available for syntax highlighting CSS")
        return ""
    except Exception as e:
        logger.error(f"Failed to generate Pygments CSS: {e}")
        return ""


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2 Compliance (Rule #1)
# =============================================================================


def create_markdown_renderer(
    base_path: str = "/wiki",
    logging_manager: Optional[Any] = None,
) -> MarkdownRenderer:
    """
    Factory function for MarkdownRenderer (Clean Architecture v5.2 Pattern).
    
    This is the ONLY way to create a MarkdownRenderer instance.
    Direct instantiation should be avoided in production code.
    
    Args:
        base_path: Base path for internal wiki links
        logging_manager: Optional logging manager
        
    Returns:
        Configured MarkdownRenderer instance
        
    Example:
        >>> renderer = create_markdown_renderer()
        >>> html = renderer.render("# Hello World")
        >>> html, toc = renderer.render_with_toc(content)
    """
    return MarkdownRenderer(
        base_path=base_path,
        logging_manager=logging_manager,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "MarkdownRenderer",
    "create_markdown_renderer",
    "get_wiki_styles",
    "get_pygments_styles",
]
