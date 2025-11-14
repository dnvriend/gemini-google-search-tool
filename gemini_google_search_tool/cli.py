"""CLI entry point for gemini-google-search-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_google_search_tool.utils import get_greeting


@click.command()
@click.version_option(version="0.1.0")
def main() -> None:
    """A CLI that enables you to query Gemini with Google Search grounding, connecting the model to real-time web content"""
    click.echo(get_greeting())


if __name__ == "__main__":
    main()
