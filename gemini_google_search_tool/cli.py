"""CLI entry point for gemini-google-search-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_google_search_tool.commands import query


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """A CLI that enables you to query Gemini with Google Search grounding.

    This tool connects Gemini to real-time web content, providing
    accurate, up-to-date answers with verifiable sources.

    Environment Variables:
        GEMINI_API_KEY    Required API key for Gemini authentication

    Examples:

    \b
        # Query with Google Search grounding
        gemini-google-search-tool query "Who won euro 2024?"

    \b
        # Query with inline citations
        gemini-google-search-tool query "Latest AI news" --add-citations

    \b
        # Read prompt from stdin
        echo "Climate change updates" | gemini-google-search-tool query --stdin

    For detailed help on each command, run:
        gemini-google-search-tool COMMAND --help
    """
    pass


# Register commands
main.add_command(query)


if __name__ == "__main__":
    main()
