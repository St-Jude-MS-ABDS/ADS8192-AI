"""Command-line interface for biosci-chat."""

from __future__ import annotations

import click

from biosci_chat.client import BiosciClient
from biosci_chat.prompts import get_system_prompt, list_domains

_EXIT_TOKENS = {"exit", "quit", "/exit", "/quit"}


@click.group()
def cli() -> None:
    """biosci-chat — AI-powered biology question answering."""


@cli.command()
@click.argument("question")
@click.option(
    "--domain",
    "-d",
    default="general",
    show_default=True,
    help=f"Biology sub-domain. Choices: {', '.join(list_domains())}",
)
@click.option(
    "--model", "-m", default="gpt-4o-mini", show_default=True, help="OpenAI model to use."
)
@click.option(
    "--stream/--no-stream",
    default=True,
    show_default=True,
    help="Stream the response token by token.",
)
def ask(question: str, domain: str, model: str, stream: bool) -> None:
    """Ask a biology QUESTION and print the answer.

    Parameters
    ----------
    question : str
        The biology question to ask.
    domain : str
        Biology sub-domain to specialise the response.
    model : str
        OpenAI model identifier.
    stream : bool
        Whether to stream the response token by token.
    """
    client = BiosciClient(model=model)
    if stream:
        for chunk in client.stream(question, domain=domain):
            click.echo(chunk, nl=False)
        click.echo()
    else:
        click.echo(client.ask(question, domain=domain))


@cli.command()
@click.argument("message", required=False, default=None)
@click.option(
    "--domain",
    "-d",
    default="general",
    show_default=True,
    help=f"Biology sub-domain. Choices: {', '.join(list_domains())}",
)
@click.option(
    "--model", "-m", default="gpt-4o-mini", show_default=True, help="OpenAI model to use."
)
@click.option(
    "--stream/--no-stream",
    default=True,
    show_default=True,
    help="Stream responses token by token.",
)
def chat(message: str | None, domain: str, model: str, stream: bool) -> None:
    """Start an interactive biology chat session.

    Optionally seed the first turn with MESSAGE. Type 'exit' or 'quit' to end the session.
    """
    client = BiosciClient(model=model)
    messages: list[dict[str, str]] = [{"role": "system", "content": get_system_prompt(domain)}]

    def _send(user_text: str) -> str:
        messages.append({"role": "user", "content": user_text})
        snapshot = list(messages)
        if stream:
            reply_parts: list[str] = []
            for chunk in client.stream_messages(snapshot):
                click.echo(chunk, nl=False)
                reply_parts.append(chunk)
            click.echo()
            reply = "".join(reply_parts)
        else:
            reply = client.reply_messages(snapshot)
            click.echo(reply)
        messages.append({"role": "assistant", "content": reply})
        return reply

    if message:
        _send(message)

    while True:
        try:
            line = input("You: ")
        except EOFError:
            break
        stripped = line.strip()
        if stripped.lower() in _EXIT_TOKENS:
            break
        if not stripped:
            continue
        _send(stripped)


@cli.command(name="list-domains")
def list_domains_cmd() -> None:
    """List all available biology sub-domains.

    Prints each domain name on a separate line.
    """
    for d in list_domains():
        click.echo(f"  {d}")


if __name__ == "__main__":
    cli()
