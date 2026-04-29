"""Tests for biosci_chat.client module."""

from __future__ import annotations

import pytest

from biosci_chat.client import BiosciClient


def test_ask_returns_mocked_response(mock_client):
    """ask() returns the string content from the mocked API response."""
    client = BiosciClient()
    result = client.ask("What is BRCA1?")
    assert result == "BRCA1 is a tumour suppressor gene located on chromosome 17."


def test_ask_calls_api_with_user_message(mock_client):
    """ask() passes the question as a user message to the API."""
    client = BiosciClient()
    client.ask("What is DNA?")
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = call_kwargs["messages"]
    user_messages = [m for m in messages if m["role"] == "user"]
    assert len(user_messages) == 1
    assert user_messages[0]["content"] == "What is DNA?"


def test_ask_uses_system_prompt_for_domain(mock_client):
    """ask() includes a system message with the correct domain prompt."""
    client = BiosciClient()
    client.ask("What is a SNP?", domain="genomics")
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = call_kwargs["messages"]
    system_messages = [m for m in messages if m["role"] == "system"]
    assert len(system_messages) == 1
    assert "genomics" in system_messages[0]["content"].lower()


def test_ask_raises_for_invalid_domain(mock_client):
    """ask() propagates ValueError from get_system_prompt for bad domains."""
    client = BiosciClient()
    with pytest.raises(ValueError, match="astrology"):
        client.ask("What is a star?", domain="astrology")


def test_default_model_is_gpt4o_mini(mock_client):
    """BiosciClient uses gpt-4o-mini as the default model."""
    client = BiosciClient()
    assert client.model == "gpt-4o-mini"


def test_custom_model_is_stored(mock_client):
    """BiosciClient stores a custom model name."""
    client = BiosciClient(model="gpt-4o")
    assert client.model == "gpt-4o"


def test_ask_passes_correct_model_to_api(mock_client):
    """ask() passes the configured model name to the API call."""
    client = BiosciClient(model="gpt-4o")
    client.ask("What is RNA?")
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "gpt-4o"


def test_stream_yields_text_chunks(mock_client, mock_stream_chunks):
    """stream() yields non-empty string chunks from the API."""
    mock_client.chat.completions.create.return_value = iter(mock_stream_chunks)
    client = BiosciClient()
    chunks = list(client.stream("What is BRCA1?"))
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)


def test_stream_concatenates_to_full_response(mock_client, mock_stream_chunks):
    """Concatenating all stream() chunks produces the full response."""
    mock_client.chat.completions.create.return_value = iter(mock_stream_chunks)
    client = BiosciClient()
    full = "".join(client.stream("What is BRCA1?"))
    assert "BRCA1" in full


def test_reply_messages_sends_exact_messages(mock_client):
    """reply_messages() forwards the exact messages list to the API."""
    client = BiosciClient()
    messages = [
        {"role": "system", "content": "You are a biology assistant."},
        {"role": "user", "content": "What is DNA?"},
        {"role": "assistant", "content": "DNA is a molecule."},
        {"role": "user", "content": "What about RNA?"},
    ]
    result = client.reply_messages(messages)
    assert result == "BRCA1 is a tumour suppressor gene located on chromosome 17."
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["messages"] == messages


def test_stream_messages_yields_chunks(mock_client, mock_stream_chunks):
    """stream_messages() yields text chunks from the API."""
    mock_client.chat.completions.create.return_value = iter(mock_stream_chunks)
    client = BiosciClient()
    messages = [
        {"role": "system", "content": "You are a biology assistant."},
        {"role": "user", "content": "What is BRCA1?"},
    ]
    chunks = list(client.stream_messages(messages))
    assert len(chunks) > 0
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["messages"] == messages
    assert call_kwargs.get("stream") is True
