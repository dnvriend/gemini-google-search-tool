---
description: Query Gemini with Google Search grounding
argument-hint: prompt
---

Query Gemini with Google Search grounding for real-time web information with automatic citations.

## Usage

```bash
gemini-google-search-tool query "PROMPT" [OPTIONS]
```

## Arguments

- `PROMPT`: Search query (required, or use `--stdin`)
- `--stdin` / `-s`: Read prompt from stdin
- `--add-citations`: Add inline citation links to response
- `--pro`: Use gemini-2.5-pro (default: gemini-2.5-flash)
- `--text` / `-t`: Output markdown format (default: JSON)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic query
gemini-google-search-tool query "Who won euro 2024?"

# With inline citations
gemini-google-search-tool query "Latest AI news" --add-citations

# From stdin
echo "Climate change" | gemini-google-search-tool query --stdin

# Pro model with debug output
gemini-google-search-tool query "Quantum computing" --pro -vv
```

## Output

**JSON (default):**
- `response_text`: AI response with grounding
- `citations`: Array of {index, uri, title}
- `grounding_metadata`: Search queries and supports (with `-vv`)

**Markdown (`--text`):**
- Response text followed by citations list
