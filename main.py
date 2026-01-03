#!/usr/bin/env python3
"""
Ash-Dash: Crisis Detection Dashboard for The Alphabet Cartel Discord Community
CORE PRINCIPLE:
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-Dash is a CRISIS DETECTION DASHBOARD that:
1. **PRIMARY**:
2. **SECONDARY**:
3. **TERTIARY**:
4. **PURPOSE**:
********************************************************************************
Main Entry Point for Ash-Dash Service
---
FILE VERSION: v5.0
LAST MODIFIED: 2026-1-22026-01-02
PHASE: Phase 1
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

USAGE:
    # Run with default settings
    python main.py

ENVIRONMENT VARIABLES:
"""

import logging
import os
import sys

# Module version
__version__ = "v5.0"


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Convert string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    # Reduce noise from third-party libraries
    # logging.getLogger("uvicorn").setLevel(logging.WARNING)
    # logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at {log_level} level")


def main() -> None:
    """
    Main entry point for running the service.
    """
    # Setup logging
    setup_logging(args.log_level)

    logger = logging.getLogger(__name__)

    # Print startup banner
    logger.info("=" * 60)
    logger.info("  Ash-Bot Crisis Detection Service")
    logger.info(f"  Version: {__version__}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
