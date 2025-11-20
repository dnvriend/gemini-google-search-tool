"""CLI entry point for gemini-google-search-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click
from click.shell_completion import BashComplete, FishComplete, ZshComplete

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


@main.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script.

    SHELL: The shell type (bash, zsh, fish)

    Install instructions:

    \b
    # Bash (add to ~/.bashrc):
    eval "$(gemini-google-search-tool completion bash)"

    \b
    # Zsh (add to ~/.zshrc):
    eval "$(gemini-google-search-tool completion zsh)"

    \b
    # Fish (add to ~/.config/fish/completions/gemini-google-search-tool.fish):
    gemini-google-search-tool completion fish > \\
        ~/.config/fish/completions/gemini-google-search-tool.fish

    Examples:

    \b
        # Generate bash completion
        gemini-google-search-tool completion bash

    \b
        # Install bash completion persistently
        echo 'eval "$(gemini-google-search-tool completion bash)"' >> ~/.bashrc

    \b
        # Install zsh completion persistently
        echo 'eval "$(gemini-google-search-tool completion zsh)"' >> ~/.zshrc

    \b
        # Install fish completion (automatic loading)
        mkdir -p ~/.config/fish/completions
        gemini-google-search-tool completion fish > \\
            ~/.config/fish/completions/gemini-google-search-tool.fish
    """
    ctx = click.get_current_context()
    prog_name = ctx.find_root().info_name or "gemini-google-search-tool"

    # Get the appropriate completion class
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    completion_class = completion_classes.get(shell)
    if completion_class:
        completer = completion_class(
            cli=ctx.find_root().command,
            ctx_args={},
            prog_name=prog_name,
            complete_var=f"_{prog_name.upper().replace('-', '_')}_COMPLETE",
        )
        click.echo(completer.source())
    else:
        raise click.BadParameter(f"Unsupported shell: {shell}")


if __name__ == "__main__":
    main()
