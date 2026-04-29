"""Tests for biosci_chat.cli module."""

from __future__ import annotations

from unittest.mock import MagicMock

from click.testing import CliRunner

from biosci_chat.cli import cli
from biosci_chat.prompts import list_domains


def test_ask_no_stream_prints_response(mock_client):
    """ask --no-stream prints the mocked response to stdout."""
    runner = CliRunner()
    result = runner.invoke(cli, ["ask", "What is DNA?", "--no-stream"])
    assert result.exit_code == 0
    assert "BRCA1" in result.output


def test_ask_invalid_domain_exits_nonzero(mock_client):
    """ask with an invalid --domain exits with a non-zero code."""
    runner = CliRunner()
    result = runner.invoke(cli, ["ask", "What is a star?", "--domain", "astrology", "--no-stream"])
    assert result.exit_code != 0


def test_list_domains_prints_all_domains():
    """list-domains prints every configured biology domain."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list-domains"])
    assert result.exit_code == 0
    for domain in list_domains():
        assert domain in result.output


def test_ask_uses_default_domain(mock_client):
    """ask without --domain uses the 'general' domain."""
    runner = CliRunner()
    result = runner.invoke(cli, ["ask", "What is a cell?", "--no-stream"])
    assert result.exit_code == 0
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = call_kwargs["messages"]
    system_content = next(m["content"] for m in messages if m["role"] == "system")
    assert "biology assistant" in system_content.lower()


def _make_response(text: str) -> MagicMock:
    choice = MagicMock()
    choice.message.content = text
    resp = MagicMock()
    resp.choices = [choice]
    return resp


def test_chat_multi_turn_no_stream(mock_client):
    """chat --no-stream handles two turns and includes history on the second call."""
    turn1 = _make_response("DNA is a double helix.")
    turn2 = _make_response("RNA is single-stranded.")
    mock_client.chat.completions.create.side_effect = [turn1, turn2]

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["chat", "--no-stream"],
        input="What is DNA?\nWhat is RNA?\nexit\n",
    )

    assert result.exit_code == 0
    assert "DNA is a double helix." in result.output
    assert "RNA is single-stranded." in result.output

    assert mock_client.chat.completions.create.call_count == 2

    second_call_messages = mock_client.chat.completions.create.call_args_list[1].kwargs["messages"]
    roles = [m["role"] for m in second_call_messages]
    assert roles == ["system", "user", "assistant", "user"]
    assert second_call_messages[2]["content"] == "DNA is a double helix."


def test_chat_seeded_message_no_stream(mock_client):
    """chat with an initial MESSAGE argument answers it before entering the loop."""
    mock_client.chat.completions.create.return_value = _make_response(
        "BRCA1 is a tumour suppressor."
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["chat", "What is BRCA1?", "--no-stream"],
        input="exit\n",
    )

    assert result.exit_code == 0
    assert "BRCA1 is a tumour suppressor." in result.output
    assert mock_client.chat.completions.create.call_count == 1


def test_chat_invalid_domain_exits_nonzero(mock_client):
    """chat with an invalid --domain exits with a non-zero code."""
    runner = CliRunner()
    result = runner.invoke(cli, ["chat", "--domain", "astrology", "--no-stream"], input="exit\n")
    assert result.exit_code != 0


def test_chat_exits_on_eof(mock_client):
    """chat exits cleanly when the input stream ends (EOF)."""
    mock_client.chat.completions.create.return_value = _make_response("Mitosis divides cells.")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["chat", "--no-stream"],
        input="What is mitosis?\n",
    )

    assert result.exit_code == 0
    assert "Mitosis divides cells." in result.output
