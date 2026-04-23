"""Command-line interface for biosci-chat."""

from __future__ import annotations

import click

from biosci_chat.client import BiosciClient
from biosci_chat.prompts import list_domains


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
@click.option("--model", "-m", default="gpt-4o-mini", show_default=True, help="OpenAI model to use.")
@click.option("--stream/--no-stream", default=True, show_default=True, help="Stream the response token by token.")
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


@cli.command(name="list-domains")
def list_domains_cmd() -> None:
    """List all available biology sub-domains.

    Prints each domain name on a separate line.
    """
    for d in list_domains():
        click.echo(f"  {d}")


if __name__ == "__main__":
    cli()
