---
description: Generate shell completion scripts
argument-hint: shell
---

Generate shell completion script for bash, zsh, or fish.

## Usage

```bash
gemini-google-search-tool completion {bash|zsh|fish}
```

## Arguments

- `SHELL`: Shell type (bash, zsh, or fish)

## Examples

```bash
# Generate bash completion
gemini-google-search-tool completion bash

# Install bash completion
eval "$(gemini-google-search-tool completion bash)"

# Install zsh completion
eval "$(gemini-google-search-tool completion zsh)"

# Install fish completion
gemini-google-search-tool completion fish > ~/.config/fish/completions/gemini-google-search-tool.fish
```

## Output

Shell-specific completion script to stdout.
