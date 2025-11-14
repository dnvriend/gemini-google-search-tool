# gemini-google-search-tool - Developer Guide

## Overview

`gemini-google-search-tool` is a professional CLI tool and Python library for querying Gemini with Google Search grounding. It provides real-time web search capabilities with automatic citations.

### Tech Stack

- **Python 3.14+** - Modern Python with latest syntax (dict/list over Dict/List)
- **uv** - Fast Python package manager for dependency management
- **mise** - Development environment manager (optional)
- **click** - CLI framework for building commands
- **google-genai** - Official Gemini Python SDK
- **ruff** - Linting and formatting
- **mypy** - Strict type checking
- **pytest** - Testing framework

## Architecture

### Module Structure

```
gemini-google-search-tool/
├── gemini_google_search_tool/
│   ├── __init__.py              # Public API exports for library usage
│   │                            # Exports: GeminiClient, query_with_grounding,
│   │                            # SearchResponse, Citation, etc.
│   │
│   ├── cli.py                   # CLI entry point (Click group)
│   │                            # Registers all commands, handles --version
│   │
│   ├── core/                    # Core library functions (importable)
│   │   ├── __init__.py          # Core module exports
│   │   ├── client.py            # Gemini client management
│   │   │                        # - GeminiClient class
│   │   │                        # - API key validation
│   │   │                        # - Client initialization
│   │   │
│   │   └── search.py            # Search and citation processing
│   │                            # - query_with_grounding()
│   │                            # - add_inline_citations()
│   │                            # - SearchResponse dataclass
│   │                            # - Citation, GroundingSegment dataclasses
│   │
│   ├── commands/                # CLI command implementations
│   │   ├── __init__.py          # Command exports
│   │   └── query_commands.py   # Query command with Click decorators
│   │                            # - CLI wrapper around core functions
│   │                            # - Handles user input, output formatting
│   │                            # - Error handling and exit codes
│   │
│   └── utils.py                 # Shared utilities
│                                # - Output formatting (JSON, text)
│                                # - Input validation
│                                # - Verbose logging
│
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_utils.py            # Utility function tests
│
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # User-facing documentation
├── CLAUDE.md                    # This file - developer guide
├── LICENSE                      # MIT License
├── .mise.toml                   # mise configuration
└── .gitignore                   # Git ignore rules
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/` contains business logic independent of CLI
   - `commands/` contains CLI-specific code (Click decorators, formatting)
   - `utils.py` provides shared utilities
   - Clear boundaries between library and CLI code

2. **Exception-Based Error Handling**
   - Core functions raise custom exceptions (`GeminiClientError`, `SearchError`)
   - CLI commands catch exceptions at the boundary
   - CLI formats errors and sets appropriate exit codes
   - Never use `sys.exit()` in core library functions

3. **Importable Library**
   - `__init__.py` exposes public API for library usage
   - Users can `from gemini_google_search_tool import GeminiClient, query_with_grounding`
   - Core functions work independently of CLI
   - Dataclasses (`SearchResponse`, `Citation`) provide structured data

4. **Type Safety**
   - Strict mypy checking enabled
   - Comprehensive type hints on all functions
   - Modern Python syntax: `dict[str, Any]` instead of `Dict[str, Any]`
   - No `Any` types unless absolutely necessary

5. **Composability**
   - JSON output to stdout (easily parseable)
   - Logs and verbose output to stderr
   - Supports piping: `echo "query" | tool query --stdin`
   - Exit codes: 0 for success, 1 for errors

## Development Commands

### Quick Start

```bash
# Clone and setup
git clone https://github.com/dnvriend/gemini-google-search-tool.git
cd gemini-google-search-tool

# Install dependencies
make install

# Run all checks
make check
```

### Quality Checks

```bash
# Format code (auto-fix)
make format

# Lint code (check without fixing)
make lint

# Type check with mypy (strict mode)
make typecheck

# Run tests
make test

# Run all checks (lint + typecheck + test)
make check

# Full pipeline (format + check + build + install-global)
make pipeline
```

### Build and Install

```bash
# Build wheel package
make build

# Install globally with uv tool
make install-global

# Clean build artifacts
make clean
```

### Local Development

```bash
# Run CLI locally without installing
uv run gemini-google-search-tool query "test query"

# Run specific test file
uv run pytest tests/test_utils.py -v

# Run tests with coverage
uv run pytest tests/ --cov=gemini_google_search_tool
```

## Code Standards

### Type Hints

All functions must have complete type hints:

```python
# ✅ Good
def query_with_grounding(
    client: GeminiClient,
    prompt: str,
    model: str = "gemini-2.5-flash",
) -> SearchResponse:
    ...

# ❌ Bad (no return type)
def query_with_grounding(client: GeminiClient, prompt: str, model: str = "gemini-2.5-flash"):
    ...
```

### Modern Python Syntax

Use Python 3.14+ syntax:

```python
# ✅ Good (Python 3.10+)
def process_data(items: list[str]) -> dict[str, int]:
    ...

# ❌ Bad (old syntax)
from typing import Dict, List
def process_data(items: List[str]) -> Dict[str, int]:
    ...
```

### Docstrings

Use Google-style docstrings:

```python
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
    ...
```

### Error Handling

Core functions raise exceptions, CLI handles them:

```python
# In core/search.py
def query_with_grounding(...) -> SearchResponse:
    try:
        response = client.client.models.generate_content(...)
        return SearchResponse(...)
    except Exception as e:
        raise SearchError(f"Query failed: {str(e)}") from e

# In commands/query_commands.py
@click.command()
def query(...):
    try:
        response = query_with_grounding(client, prompt, model)
        output_json({"response_text": response.response_text})
    except SearchError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
```

## CLI Commands

### Command: `query`

Query Gemini with Google Search grounding for real-time web information.

**Usage:**
```bash
gemini-google-search-tool query [PROMPT] [OPTIONS]
```

**Arguments:**
- `PROMPT` - Query prompt (positional, optional if `--stdin` is used)

**Options:**
- `--stdin`, `-s` - Read prompt from stdin (overrides PROMPT)
- `--add-citations` - Add inline citations to response text
- `--pro` - Use gemini-2.5-pro model (default: gemini-2.5-flash)
- `--text`, `-t` - Output markdown format instead of JSON
- `--verbose`, `-v` - Enable verbose output (includes grounding metadata)

**Examples:**

```bash
# Basic query
gemini-google-search-tool query "Who won euro 2024?"

# With citations
gemini-google-search-tool query "Latest AI news" --add-citations

# From stdin
echo "Climate change updates" | gemini-google-search-tool query --stdin

# Markdown output
gemini-google-search-tool query "Quantum computing" --text

# Pro model with verbose output
gemini-google-search-tool query "Complex analysis" --pro --verbose
```

**Output Format (JSON):**
```json
{
  "response_text": "...",
  "citations": [
    {"index": 1, "uri": "https://...", "title": "..."}
  ],
  "grounding_metadata": {
    "web_search_queries": ["..."],
    "grounding_chunks": [...],
    "grounding_supports": [...]
  }
}
```

*Note: Citations are always included in JSON output. The `--add-citations` flag adds inline citation links to the response_text. The `grounding_metadata` is only included with `--verbose`.*

**Output Format (--text):**
```markdown
<response text in markdown>

## Citations

1. [Title](https://...)
2. [Another Title](https://...)
```

## Library Usage

### Basic Usage

```python
from gemini_google_search_tool import GeminiClient, query_with_grounding

# Initialize client (reads GEMINI_API_KEY from environment)
client = GeminiClient()

# Query with grounding
response = query_with_grounding(
    client=client,
    prompt="Who won euro 2024?",
    model="gemini-2.5-flash",
)

# Access response
print(response.response_text)
print(f"Citations: {len(response.citations)}")

# Access citations
for citation in response.citations:
    print(f"[{citation.index}] {citation.title}: {citation.uri}")
```

### With Inline Citations

```python
from gemini_google_search_tool import (
    GeminiClient,
    query_with_grounding,
    add_inline_citations,
)

client = GeminiClient()
response = query_with_grounding(client, "Latest AI developments")

# Add inline citations
if response.grounding_segments:
    text_with_citations = add_inline_citations(
        response.response_text,
        response.grounding_segments,
        response.citations,
    )
    print(text_with_citations)
```

### Error Handling

```python
from gemini_google_search_tool import GeminiClient, GeminiClientError, SearchError

try:
    client = GeminiClient()
    response = query_with_grounding(client, "Your query")
except GeminiClientError as e:
    print(f"Client error: {e}")
    # Handle authentication or configuration errors
except SearchError as e:
    print(f"Search error: {e}")
    # Handle query execution errors
```

### Custom API Key

```python
from gemini_google_search_tool import GeminiClient

# Provide API key directly (instead of environment variable)
client = GeminiClient(api_key="your-api-key-here")
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_utils.py::test_validate_prompt_with_argument -v

# Run with coverage
uv run pytest tests/ --cov=gemini_google_search_tool --cov-report=html
```

### Test Structure

Tests are located in `tests/` directory:

```
tests/
├── __init__.py
└── test_utils.py        # Tests for utility functions
```

### Writing Tests

Follow pytest conventions:

```python
import pytest
from gemini_google_search_tool.utils import validate_prompt

def test_validate_prompt_with_argument() -> None:
    """Test that validate_prompt returns the provided prompt."""
    prompt = "Who won euro 2024?"
    result = validate_prompt(prompt, use_stdin=False)
    assert result == prompt
    assert isinstance(result, str)

def test_validate_prompt_no_input_raises_error() -> None:
    """Test that validate_prompt raises ValueError when no input provided."""
    with pytest.raises(ValueError, match="No prompt provided"):
        validate_prompt(None, use_stdin=False)
```

## Important Notes

### Core Dependencies

- **click** (>=8.1.7) - CLI framework
  - Documentation: https://click.palletsprojects.com/
  - Used for command decorators, arguments, options

- **google-genai** (>=1.0.0) - Official Gemini Python SDK
  - Documentation: https://ai.google.dev/gemini-api/docs
  - Used for Gemini API client and types
  - Handles authentication, requests, and response parsing

### Authentication

The tool requires a `GEMINI_API_KEY` environment variable:

```bash
# Set environment variable
export GEMINI_API_KEY='your-api-key-here'

# Or retrieve from macOS keychain
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

Get a free API key: https://aistudio.google.com/app/apikey

### Client Implementation

The `GeminiClient` class wraps the `genai.Client`:

```python
class GeminiClient:
    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise GeminiClientError(
                "GEMINI_API_KEY environment variable is required. "
                "Set it with: export GEMINI_API_KEY='your-api-key'"
            )
        self._client = genai.Client(api_key=api_key)

    @property
    def client(self) -> genai.Client:
        return self._client
```

### Search Implementation

The `query_with_grounding()` function:

1. Creates a `Tool` with `GoogleSearch()`
2. Configures `GenerateContentConfig` with the tool
3. Calls `client.models.generate_content()` with the config
4. Extracts response text from candidates
5. Parses grounding metadata (citations, queries, supports)
6. Returns a structured `SearchResponse` dataclass

### Citation Processing

The `add_inline_citations()` function:

1. Receives response text, grounding segments, and citations
2. Sorts segments by end_index (descending) to avoid index shifting
3. For each segment, creates citation links like `[1](uri1), [2](uri2)`
4. Inserts citation strings at segment end positions
5. Returns modified text with inline citations

### Version Synchronization

**CRITICAL**: Keep version consistent across three locations:

1. `pyproject.toml` - `[project]` section: `version = "0.1.0"`
2. `cli.py` - `@click.version_option(version="0.1.0")`
3. `__init__.py` - `__version__ = "0.1.0"`

When updating version, change all three files.

## Known Issues & Future Fixes

Currently no known issues with the SDK or implementation.

## Resources

- **Google Search Grounding**: https://ai.google.dev/gemini-api/docs/grounding
- **Gemini API**: https://ai.google.dev/gemini-api/docs
- **google-genai SDK**: https://github.com/googleapis/python-genai
- **Click Documentation**: https://click.palletsprojects.com/
- **uv Package Manager**: https://github.com/astral-sh/uv

---

Generated with [Claude Code](https://www.anthropic.com/claude/code)
