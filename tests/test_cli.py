"""Tests for biosci_chat.cli module."""

from __future__ import annotations

from click.testing import CliRunner

from biosci_chat.cli import cli


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
    """list-domains prints all four biology domains."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list-domains"])
    assert result.exit_code == 0
    for domain in ["general", "genomics", "proteomics", "pathways"]:
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
