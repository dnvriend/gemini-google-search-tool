"""Google Search grounding and citation processing.

This module handles querying Gemini with Google Search grounding
and processing citation metadata.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass

from google.genai import types

from gemini_google_search_tool.core.client import GeminiClient


class SearchError(Exception):
    """Exception raised for search errors."""

    pass


@dataclass
class Citation:
    """Represents a single citation source.

    Attributes:
        index: Citation number (1-based)
        uri: Web URI of the source
        title: Title of the source (may be empty)
    """

    index: int
    uri: str
    title: str


@dataclass
class GroundingSegment:
    """Represents a text segment with grounding support.

    Attributes:
        start_index: Starting character index in response text
        end_index: Ending character index in response text
        text: The actual text segment
        chunk_indices: List of citation indices supporting this segment
    """

    start_index: int
    end_index: int
    text: str
    chunk_indices: list[int]


@dataclass
class SearchResponse:
    """Represents a complete search response with grounding metadata.

    Attributes:
        response_text: The main response text from Gemini
        citations: List of citation sources
        web_search_queries: List of search queries executed (if available)
        grounding_segments: List of text segments with grounding support (if available)
    """

    response_text: str
    citations: list[Citation]
    web_search_queries: list[str] | None = None
    grounding_segments: list[GroundingSegment] | None = None


def query_with_grounding(
    client: GeminiClient,
    prompt: str,
    model: str = "gemini-2.5-flash",
) -> SearchResponse:
    """Query Gemini with Google Search grounding.

    Args:
        client: Initialized GeminiClient instance
        prompt: The query prompt
        model: Model to use (default: gemini-2.5-flash)

    Returns:
        SearchResponse containing response text and grounding metadata

    Raises:
        SearchError: If the query fails or returns invalid response
    """
    try:
        # Build Google Search tool
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool])

        # Generate content
        response = client.client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        # Extract response text
        response_text = ""
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                response_text = "".join(
                    part.text
                    for part in candidate.content.parts
                    if hasattr(part, "text") and part.text is not None
                )

        # Extract grounding metadata
        citations: list[Citation] = []
        web_search_queries: list[str] | None = None
        grounding_segments: list[GroundingSegment] | None = None

        if (
            response.candidates
            and len(response.candidates) > 0
            and hasattr(response.candidates[0], "grounding_metadata")
        ):
            grounding_metadata = response.candidates[0].grounding_metadata

            if grounding_metadata:
                # Extract citations
                chunks = getattr(grounding_metadata, "grounding_chunks", [])
                for i, chunk in enumerate(chunks):
                    uri = None
                    title = None

                    if hasattr(chunk, "web") and chunk.web:
                        uri = getattr(chunk.web, "uri", None)
                        title = getattr(chunk.web, "title", None)
                    elif hasattr(chunk, "uri"):
                        uri = chunk.uri
                        title = getattr(chunk, "title", None)

                    if uri:
                        citations.append(Citation(index=i + 1, uri=uri, title=title or ""))

                # Extract web search queries
                queries = getattr(grounding_metadata, "web_search_queries", [])
                if queries:
                    web_search_queries = queries

                # Extract grounding supports
                supports = getattr(grounding_metadata, "grounding_supports", [])
                if supports:
                    segments: list[GroundingSegment] = []
                    for support in supports:
                        segment = getattr(support, "segment", None)
                        chunk_indices = getattr(support, "grounding_chunk_indices", [])

                        if segment:
                            segments.append(
                                GroundingSegment(
                                    start_index=getattr(segment, "start_index", 0),
                                    end_index=getattr(segment, "end_index", 0),
                                    text=getattr(segment, "text", ""),
                                    chunk_indices=chunk_indices,
                                )
                            )
                    if segments:
                        grounding_segments = segments

        return SearchResponse(
            response_text=response_text,
            citations=citations,
            web_search_queries=web_search_queries,
            grounding_segments=grounding_segments,
        )

    except Exception as e:
        raise SearchError(f"Query failed: {str(e)}") from e


def add_inline_citations(
    response_text: str,
    grounding_segments: list[GroundingSegment] | None,
    citations: list[Citation],
) -> str:
    """Add inline citations to response text.

    Processes grounding segments to insert citation links in the format
    [1](uri1), [2](uri2) at appropriate positions in the text.

    Args:
        response_text: The original response text
        grounding_segments: List of text segments with grounding support
        citations: List of available citations

    Returns:
        Response text with inline citations added
    """
    if not grounding_segments or not citations:
        return response_text

    # Create citation URI lookup
    citation_uris = {c.index: c.uri for c in citations}

    # Sort segments by end_index in descending order to avoid shifting issues
    sorted_segments = sorted(grounding_segments, key=lambda s: s.end_index, reverse=True)

    text = response_text
    for segment in sorted_segments:
        if not segment.chunk_indices:
            continue

        # Create citation string like [1](link1), [2](link2)
        citation_links = []
        for chunk_idx in segment.chunk_indices:
            # chunk_indices are 0-based, citation index is 1-based
            citation_idx = chunk_idx + 1
            uri = citation_uris.get(citation_idx)
            if uri:
                citation_links.append(f"[{citation_idx}]({uri})")

        if citation_links:
            citation_string = ", ".join(citation_links)
            text = text[: segment.end_index] + citation_string + text[segment.end_index :]

    return text
