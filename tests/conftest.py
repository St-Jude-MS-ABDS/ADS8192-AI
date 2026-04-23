"""Shared pytest fixtures for biosci-chat tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_openai_response():
    """Return a mock OpenAI ChatCompletion response object."""
    mock_choice = MagicMock()
    mock_choice.message.content = "BRCA1 is a tumour suppressor gene located on chromosome 17."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def mock_stream_chunks():
    """Return a list of mock streaming chunk objects."""
    chunks = []
    for text in ["BRCA1 ", "is a ", "tumour ", "suppressor."]:
        chunk = MagicMock()
        chunk.choices[0].delta.content = text
        chunks.append(chunk)
    return chunks


@pytest.fixture
def mock_client(mock_openai_response, mock_stream_chunks):
    """Patch openai.OpenAI so no real API calls are made.

    Yields
    ------
    MagicMock
        The mock OpenAI client instance.
    """
    with patch("biosci_chat.client.OpenAI") as mock_openai_cls:
        mock_instance = MagicMock()
        mock_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_instance
        yield mock_instance
