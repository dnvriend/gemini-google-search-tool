"""gemini-google-search-tool CLI and library.

A CLI that enables you to query Gemini with Google Search grounding,
connecting the model to real-time web content.

This package provides both a CLI tool and a Python library for querying
Gemini with Google Search grounding capabilities.

CLI Usage:
    gemini-google-search-tool query "Who won euro 2024?"

Library Usage:
    from gemini_google_search_tool import GeminiClient, query_with_grounding

    client = GeminiClient()
    response = query_with_grounding(client, "Who won euro 2024?")
    print(response.response_text)

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

__version__ = "0.1.0"

# Public API exports for library usage
from gemini_google_search_tool.core.client import GeminiClient, GeminiClientError
from gemini_google_search_tool.core.search import (
    Citation,
    GroundingSegment,
    SearchError,
    SearchResponse,
    add_inline_citations,
    query_with_grounding,
)

__all__ = [
    "__version__",
    "GeminiClient",
    "GeminiClientError",
    "SearchError",
    "SearchResponse",
    "Citation",
    "GroundingSegment",
    "query_with_grounding",
    "add_inline_citations",
]
