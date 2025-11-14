"""Gemini API client management.

This module handles Gemini client initialization and configuration.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os

from google import genai


class GeminiClientError(Exception):
    """Exception raised for Gemini client errors."""

    pass


class GeminiClient:
    """Manages Gemini API client instance.

    This class handles client initialization, API key validation,
    and provides a singleton-like interface for the Gemini client.

    Attributes:
        _client: The underlying genai.Client instance

    Raises:
        GeminiClientError: If GEMINI_API_KEY environment variable is not set
    """

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize Gemini client.

        Args:
            api_key: Optional API key. If not provided, reads from
                    GEMINI_API_KEY environment variable.

        Raises:
            GeminiClientError: If API key is not provided and environment
                             variable is not set.
        """
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
        """Get the underlying Gemini client.

        Returns:
            The genai.Client instance
        """
        return self._client
