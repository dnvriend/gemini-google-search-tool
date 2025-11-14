"""Core library functions for gemini-google-search-tool.

This module contains the core business logic independent of CLI.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_google_search_tool.core.client import GeminiClient
from gemini_google_search_tool.core.search import (
    SearchResponse,
    add_inline_citations,
    query_with_grounding,
)

__all__ = [
    "GeminiClient",
    "SearchResponse",
    "query_with_grounding",
    "add_inline_citations",
]
