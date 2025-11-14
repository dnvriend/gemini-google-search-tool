"""Tests for gemini_google_search_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

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


def test_validate_prompt_empty_string_raises_error() -> None:
    """Test that validate_prompt raises ValueError for empty string."""
    with pytest.raises(ValueError, match="No prompt provided"):
        validate_prompt("", use_stdin=False)
