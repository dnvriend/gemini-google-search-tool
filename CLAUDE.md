# gemini-google-search-tool - Project Specification

## Goal

A CLI that enables you to query Gemini with Google Search grounding, connecting the model to real-time web content

## What is gemini-google-search-tool?

`gemini-google-search-tool` is a command-line utility built with modern Python tooling and best practices.

## Technical Requirements

### Runtime

- Python 3.14+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework

## CLI Arguments

```bash
gemini-google-search-tool [OPTIONS]
```

### Options

- `--help` / `-h` - Show help message
- `--version` - Show version

## Project Structure

```
gemini-google-search-tool/
├── gemini_google_search_tool/
│   ├── __init__.py
│   ├── cli.py           # Click CLI entry point
│   └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml       # Project configuration
├── README.md            # User documentation
├── CLAUDE.md            # This file
├── Makefile             # Development commands
├── LICENSE              # MIT License
├── .mise.toml           # mise configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Run all checks
make check

# Full pipeline
make pipeline
```

## Installation Methods

### Global installation with mise

```bash
cd /path/to/gemini-google-search-tool
mise use -g python@3.14
uv sync
uv tool install .
```

After installation, `gemini-google-search-tool` command is available globally.

### Local development

```bash
uv sync
uv run gemini-google-search-tool [args]
```
