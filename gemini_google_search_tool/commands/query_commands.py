"""Query command implementation for gemini-google-search-tool.

This module implements the CLI 'query' command.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from gemini_google_search_tool.core.client import GeminiClient, GeminiClientError
from gemini_google_search_tool.core.search import (
    SearchError,
    add_inline_citations,
    query_with_grounding,
)
from gemini_google_search_tool.utils import (
    output_json,
    output_text,
    print_verbose,
    validate_prompt,
)


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "--stdin",
    "-s",
    is_flag=True,
    default=False,
    help="Read prompt from stdin (overrides PROMPT argument)",
)
@click.option(
    "--add-citations",
    is_flag=True,
    default=False,
    help="Add inline citations to the response text",
)
@click.option(
    "--pro",
    is_flag=True,
    default=False,
    help="Use gemini-2.5-pro model (default: gemini-2.5-flash)",
)
@click.option(
    "--text",
    "-t",
    is_flag=True,
    default=False,
    help="Output markdown format instead of JSON",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output (includes grounding metadata)",
)
def query(
    prompt: str | None,
    stdin: bool,
    add_citations: bool,
    pro: bool,
    text: bool,
    verbose: bool,
) -> None:
    """Query Gemini with Google Search grounding for real-time web information.

    Examples:

    \b
        # Basic query with positional argument
        gemini-google-search-tool query "Who won euro 2024?"

    \b
        # Query with inline citations
        gemini-google-search-tool query "Who won euro 2024?" \\
            --add-citations

    \b
        # Read prompt from stdin
        echo "Who won euro 2024?" | gemini-google-search-tool query --stdin

    \b
        # Use pro model with markdown output
        gemini-google-search-tool query "Latest AI developments" \\
            --pro --text

    \b
        # Verbose output with full grounding metadata
        gemini-google-search-tool query "Climate change news" \\
            --verbose

    \b
    Output Format (JSON):
        Returns JSON with structure:
        {
          "response_text": "...",
          "citations": [{"index": 1, "uri": "...", "title": "..."}],
          "grounding_metadata": {...}  // Only with --verbose
        }

    \b
    Output Format (--text):
        Returns markdown with citations:
        <response text in markdown>

        ## Citations

        1. [Title](https://...)
        2. [Another Title](https://...)
    """
    try:
        # Validate and retrieve prompt
        final_prompt = validate_prompt(prompt, stdin)

        # Initialize client
        client = GeminiClient()

        # Select model
        model = "gemini-2.5-pro" if pro else "gemini-2.5-flash"
        print_verbose(
            f"Querying with model '{model}' and Google Search grounding",
            verbose,
        )

        # Execute query
        response = query_with_grounding(
            client=client,
            prompt=final_prompt,
            model=model,
        )

        print_verbose("Query completed successfully", verbose)

        # Handle text output
        if text:
            # Add inline citations if requested
            if add_citations and response.grounding_segments:
                response.response_text = add_inline_citations(
                    response.response_text,
                    response.grounding_segments,
                    response.citations,
                )
                print_verbose("Citations added to response text", verbose)

            output_text(response)
            return

        # Handle JSON output (default)
        output: dict[str, object] = {}

        # Add inline citations if requested
        if add_citations and response.grounding_segments:
            response.response_text = add_inline_citations(
                response.response_text,
                response.grounding_segments,
                response.citations,
            )
            print_verbose("Citations added to response text", verbose)

        output["response_text"] = response.response_text

        # Add citations if available
        if response.citations:
            output["citations"] = [
                {"index": c.index, "uri": c.uri, "title": c.title} for c in response.citations
            ]

        # Add verbose metadata if requested
        if verbose:
            grounding_dict: dict[str, object] = {}

            if response.web_search_queries:
                grounding_dict["web_search_queries"] = response.web_search_queries

            if response.citations:
                grounding_dict["grounding_chunks"] = [
                    {"index": c.index, "uri": c.uri, "title": c.title} for c in response.citations
                ]

            if response.grounding_segments:
                grounding_dict["grounding_supports"] = [
                    {
                        "segment": {
                            "start_index": seg.start_index,
                            "end_index": seg.end_index,
                            "text": seg.text,
                        },
                        "grounding_chunk_indices": seg.chunk_indices,
                    }
                    for seg in response.grounding_segments
                ]

            if grounding_dict:
                output["grounding_metadata"] = grounding_dict

        output_json(output)

    except (GeminiClientError, SearchError, ValueError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Unexpected error: {str(e)}", err=True)
        sys.exit(1)
