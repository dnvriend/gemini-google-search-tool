"""Utility functions for gemini-google-search-tool.

This module provides shared utilities for output formatting,
validation, and logging.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from typing import Any

import click

from gemini_google_search_tool.core.search import SearchResponse


def print_verbose(message: str, verbose: bool | int = False) -> None:
    """Print verbose message to stderr.

    This function is deprecated. Use logging module instead.

    Args:
        message: The message to print
        verbose: Whether to print the message (bool or int count)
    """
    if verbose:
        click.echo(f"[INFO] {message}", err=True)


def output_json(data: Any) -> None:
    """Output JSON to stdout.

    Args:
        data: Data to serialize as JSON (dict or list)
    """
    click.echo(json.dumps(data, indent=2))


def output_text(response: SearchResponse) -> None:
    """Output response in markdown format.

    Outputs response text followed by a markdown-formatted citations list.

    Args:
        response: SearchResponse containing response text and citations
    """
    # Output response text (may already contain markdown from Gemini)
    click.echo(response.response_text)

    # Output citations in markdown format if available
    if response.citations:
        click.echo("\n## Citations\n")
        for citation in response.citations:
            if citation.title:
                # Format: 1. [Title](https://url)
                click.echo(f"{citation.index}. [{citation.title}]({citation.uri})")
            else:
                # Format: 1. [https://url](https://url)
                click.echo(f"{citation.index}. [{citation.uri}]({citation.uri})")


def read_stdin() -> str:
    """Read input from stdin.

    Returns:
        Content from stdin as a string

    Raises:
        ValueError: If stdin is empty or cannot be read
    """
    if sys.stdin.isatty():
        raise ValueError(
            "No input available from stdin. "
            "Use --stdin flag with piped input: echo 'question' | tool query --stdin"
        )

    content = sys.stdin.read().strip()
    if not content:
        raise ValueError(
            "Empty input received from stdin. "
            "Provide non-empty input: echo 'question' | tool query --stdin"
        )

    return content


def validate_prompt(prompt: str | None, use_stdin: bool) -> str:
    """Validate and retrieve the prompt from either argument or stdin.

    Args:
        prompt: Optional prompt from positional argument
        use_stdin: Whether to read from stdin

    Returns:
        The validated prompt string

    Raises:
        ValueError: If no prompt is provided or invalid input
    """
    if use_stdin:
        return read_stdin()

    if not prompt:
        raise ValueError(
            "No prompt provided. Either provide PROMPT argument or use --stdin flag.\n"
            "Examples:\n"
            "  gemini-google-search-tool query 'Who won euro 2024?'\n"
            "  echo 'Who won euro 2024?' | gemini-google-search-tool query --stdin"
        )

    return prompt


# Type alias for clarity
from typing import Optional  # noqa: E402, F401
