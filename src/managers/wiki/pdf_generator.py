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
PDF Generator - Generate PDFs from wiki documents using WeasyPrint
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.3-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Generate PDFs from WikiDocument objects
- Apply Ash-Dash branding and styling
- Include headers and footers with page numbers
- Optimize layout for printing

USAGE:
    from src.managers.wiki.pdf_generator import create_pdf_generator
    
    generator = create_pdf_generator()
    pdf_bytes = generator.generate(wiki_document)
    
    # Save to file
    with open("output.pdf", "wb") as f:
        f.write(pdf_bytes)

DEPENDENCIES:
    - WeasyPrint >= 60.0
    - markdown (for rendering if needed)
"""

import logging
from datetime import datetime
from io import BytesIO
from typing import Any, Optional

from .models import WikiDocument

# Module version
__version__ = "v5.0-7-7.3-1"

# Initialize fallback logger
logger = logging.getLogger(__name__)


# =============================================================================
# PDF Styles
# =============================================================================

PDF_STYLES = """
/* ==========================================================================
   Ash-Dash PDF Styles
   Optimized for printing
   ========================================================================== */

/* Page setup */
@page {
    size: letter;
    margin: 1in 0.75in 1in 0.75in;
    
    /* Header */
    @top-center {
        content: "The Alphabet Cartel - Ash-Dash Documentation";
        font-size: 9pt;
        color: #666;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5mm;
    }
    
    /* Footer with page numbers */
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }
    
    @bottom-right {
        content: "alphabetcartel.org";
        font-size: 8pt;
        color: #999;
    }
}

/* First page - no header */
@page :first {
    @top-center {
        content: none;
        border: none;
    }
}

/* Base styles */
body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}

/* Cover / Title section */
.pdf-cover {
    text-align: center;
    padding: 2in 0 1in 0;
    border-bottom: 3px solid #9333EA;
    margin-bottom: 1in;
}

.pdf-cover h1 {
    font-size: 28pt;
    color: #1a1a1a;
    margin: 0 0 0.5em 0;
    font-weight: 600;
}

.pdf-cover .subtitle {
    font-size: 14pt;
    color: #666;
    margin-bottom: 2em;
}

.pdf-cover .meta {
    font-size: 10pt;
    color: #888;
}

.pdf-cover .meta span {
    display: inline-block;
    margin: 0 1em;
}

.pdf-cover .logo {
    font-size: 12pt;
    color: #9333EA;
    margin-top: 2em;
    font-weight: 600;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #1a1a1a;
    page-break-after: avoid;
}

h1 { font-size: 22pt; color: #9333EA; }
h2 { font-size: 16pt; border-bottom: 1px solid #ddd; padding-bottom: 0.3em; }
h3 { font-size: 13pt; }
h4 { font-size: 11pt; }

/* First heading after cover */
.pdf-content > h1:first-child,
.pdf-content > h2:first-child {
    margin-top: 0;
}

/* Paragraphs */
p {
    margin: 0.8em 0;
    orphans: 3;
    widows: 3;
}

/* Links - show URL in print */
a {
    color: #9333EA;
    text-decoration: none;
}

a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 8pt;
    color: #666;
    word-break: break-all;
}

/* Don't show URL for internal links */
a[href^="/"]::after,
a[href^="#"]::after {
    content: none;
}

/* Lists */
ul, ol {
    margin: 0.8em 0;
    padding-left: 1.5em;
}

li {
    margin: 0.3em 0;
}

/* Nested lists */
li > ul, li > ol {
    margin: 0.2em 0;
}

/* Task lists */
.task-item {
    list-style: none;
    margin-left: -1.2em;
}

.task-item input[type="checkbox"] {
    margin-right: 0.5em;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th, td {
    padding: 0.5em 0.75em;
    text-align: left;
    border: 1px solid #ccc;
}

th {
    background: #f5f0ff;
    font-weight: 600;
    color: #1a1a1a;
}

tr:nth-child(even) {
    background: #fafafa;
}

/* Code - Inline */
code {
    background: #f4f4f4;
    padding: 0.15em 0.4em;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 9pt;
}

/* Code - Blocks */
pre {
    background: #1f2937;
    color: #e5e7eb;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    margin: 1em 0;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    padding: 0;
    color: inherit;
}

/* Syntax highlighting - simplified for print */
.highlight {
    background: #1f2937;
    padding: 1em;
    border-radius: 6px;
    margin: 1em 0;
    page-break-inside: avoid;
}

.highlight pre {
    margin: 0;
    padding: 0;
    background: transparent;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #9333EA;
    margin: 1em 0;
    padding: 0.5em 1em;
    background: #faf5ff;
    font-style: italic;
    page-break-inside: avoid;
}

blockquote p {
    margin: 0.3em 0;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
}

/* Definition lists */
dl {
    margin: 1em 0;
}

dt {
    font-weight: 600;
    margin-top: 0.8em;
}

dd {
    margin-left: 1.5em;
    margin-top: 0.2em;
}

/* Footer section */
.pdf-footer {
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid #ddd;
    font-size: 9pt;
    color: #666;
    text-align: center;
}

.pdf-footer a {
    color: #9333EA;
}

.pdf-footer a::after {
    content: none;
}

/* Pride flag accent */
.pride-bar {
    height: 4px;
    background: linear-gradient(
        to right,
        #E40303 0%, #E40303 16.66%,
        #FF8C00 16.66%, #FF8C00 33.33%,
        #FFED00 33.33%, #FFED00 50%,
        #008026 50%, #008026 66.66%,
        #004DFF 66.66%, #004DFF 83.33%,
        #750787 83.33%, #750787 100%
    );
    margin: 1em 0;
}

/* Page breaks */
.page-break {
    page-break-before: always;
}

h1, h2, h3 {
    page-break-after: avoid;
}

table, pre, blockquote, img {
    page-break-inside: avoid;
}
"""


# =============================================================================
# HTML Template
# =============================================================================

PDF_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Ash-Dash Documentation</title>
    <style>
{styles}
    </style>
</head>
<body>
    <!-- Cover Section -->
    <div class="pdf-cover">
        <h1>{title}</h1>
        {description_html}
        <div class="meta">
            <span><strong>Category:</strong> {category}</span>
            <span><strong>Version:</strong> {version}</span>
            {last_updated_html}
        </div>
        <div class="pride-bar"></div>
        <div class="logo">🏳️‍🌈 The Alphabet Cartel</div>
    </div>
    
    <!-- Content -->
    <div class="pdf-content">
{content}
    </div>
    
    <!-- Footer -->
    <div class="pdf-footer">
        <div class="pride-bar"></div>
        <p>
            <strong>The Alphabet Cartel</strong><br>
            <a href="https://discord.gg/alphabetcartel">discord.gg/alphabetcartel</a> |
            <a href="https://alphabetcartel.org">alphabetcartel.org</a>
        </p>
        <p>Generated on {generated_date} | Built with care for chosen family</p>
    </div>
</body>
</html>
"""


# =============================================================================
# PDF Generator Class
# =============================================================================


class PDFGenerator:
    """
    PDF Generator for wiki documents using WeasyPrint.
    
    Generates professionally styled PDFs with:
    - Ash-Dash branding
    - Headers and footers
    - Page numbers
    - Print-optimized styling
    
    Attributes:
        available: Whether WeasyPrint is available
    """
    
    def __init__(
        self,
        logging_manager: Optional[Any] = None,
    ):
        """
        Initialize PDFGenerator.
        
        Args:
            logging_manager: Optional logging manager
            
        Note:
            Use create_pdf_generator() factory function.
        """
        # Set up logging
        if logging_manager:
            self._logger = logging_manager.get_logger("pdf")
        else:
            self._logger = logger
        
        # Check WeasyPrint availability
        self._weasyprint = None
        self._available = False
        
        try:
            from weasyprint import HTML, CSS
            self._weasyprint = HTML
            self._weasyprint_css = CSS
            self._available = True
            self._logger.info(f"✅ PDFGenerator v{__version__} initialized (WeasyPrint available)")
        except ImportError as e:
            self._logger.warning(f"⚠️ WeasyPrint not available: {e}")
            self._logger.warning("PDF generation will not be available")
        except Exception as e:
            self._logger.error(f"❌ Failed to initialize WeasyPrint: {e}")
    
    @property
    def available(self) -> bool:
        """Check if PDF generation is available."""
        return self._available
    
    def generate(
        self,
        document: WikiDocument,
        include_cover: bool = True,
    ) -> bytes:
        """
        Generate PDF from a WikiDocument.
        
        Args:
            document: WikiDocument to convert to PDF
            include_cover: Whether to include cover page
            
        Returns:
            PDF file as bytes
            
        Raises:
            RuntimeError: If WeasyPrint is not available
        """
        if not self._available:
            raise RuntimeError(
                "PDF generation not available. "
                "Please install WeasyPrint and its dependencies."
            )
        
        self._logger.info(f"📄 Generating PDF for: {document.title}")
        
        # Get rendered HTML content
        content_html = document.content_html
        if not content_html:
            # Render if not already rendered
            from .markdown_renderer import create_markdown_renderer
            renderer = create_markdown_renderer(base_path="/wiki")
            content_html = renderer.render(document.content_md)
        
        # Build description HTML
        description_html = ""
        if document.description:
            description_html = f'<p class="subtitle">{document.description}</p>'
        
        # Build last updated HTML
        last_updated_html = ""
        if document.last_updated:
            last_updated_html = f'<span><strong>Last Updated:</strong> {document.last_updated}</span>'
        
        # Generate full HTML
        full_html = PDF_TEMPLATE.format(
            title=self._escape_html(document.title),
            description_html=description_html,
            category=self._escape_html(document.category),
            version=self._escape_html(document.version),
            last_updated_html=last_updated_html,
            content=content_html,
            generated_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            styles=PDF_STYLES,
        )
        
        # Generate PDF
        try:
            html_doc = self._weasyprint(string=full_html)
            pdf_bytes = html_doc.write_pdf()
            
            self._logger.info(
                f"✅ PDF generated: {len(pdf_bytes):,} bytes"
            )
            
            return pdf_bytes
            
        except Exception as e:
            self._logger.error(f"❌ PDF generation failed: {e}")
            raise RuntimeError(f"PDF generation failed: {e}") from e
    
    def generate_to_file(
        self,
        document: WikiDocument,
        output_path: str,
        include_cover: bool = True,
    ) -> str:
        """
        Generate PDF and save to file.
        
        Args:
            document: WikiDocument to convert
            output_path: Path to save PDF
            include_cover: Whether to include cover page
            
        Returns:
            Path to generated PDF file
        """
        pdf_bytes = self.generate(document, include_cover)
        
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        
        self._logger.info(f"📁 PDF saved to: {output_path}")
        
        return output_path
    
    def generate_to_stream(
        self,
        document: WikiDocument,
        include_cover: bool = True,
    ) -> BytesIO:
        """
        Generate PDF and return as BytesIO stream.
        
        Useful for streaming responses in web frameworks.
        
        Args:
            document: WikiDocument to convert
            include_cover: Whether to include cover page
            
        Returns:
            BytesIO stream containing PDF
        """
        pdf_bytes = self.generate(document, include_cover)
        stream = BytesIO(pdf_bytes)
        stream.seek(0)
        return stream
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "available" if self._available else "unavailable"
        return f"PDFGenerator(status={status})"


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2 Compliance (Rule #1)
# =============================================================================


def create_pdf_generator(
    logging_manager: Optional[Any] = None,
) -> PDFGenerator:
    """
    Factory function for PDFGenerator (Clean Architecture v5.2 Pattern).
    
    This is the ONLY way to create a PDFGenerator instance.
    Direct instantiation should be avoided in production code.
    
    Args:
        logging_manager: Optional logging manager
        
    Returns:
        Configured PDFGenerator instance
        
    Example:
        >>> generator = create_pdf_generator()
        >>> if generator.available:
        ...     pdf_bytes = generator.generate(document)
        ...     with open("output.pdf", "wb") as f:
        ...         f.write(pdf_bytes)
    """
    return PDFGenerator(logging_manager=logging_manager)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "PDFGenerator",
    "create_pdf_generator",
    "PDF_STYLES",
]
