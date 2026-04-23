"""OpenAI API client for biosci-chat."""

from __future__ import annotations

import os
from typing import Iterator

from openai import OpenAI

from biosci_chat.prompts import get_system_prompt


class BiosciClient:
    """Thin wrapper around the OpenAI chat completions API.

    Parameters
    ----------
    model : str
        OpenAI model identifier. Defaults to ``gpt-4o-mini``.
    api_key : str or None
        OpenAI API key. Falls back to the ``OPENAI_API_KEY`` environment
        variable if not provided.

    Examples
    --------
    >>> client = BiosciClient()
    >>> response = client.ask("What is CRISPR?", domain="genomics")
    >>> isinstance(response, str)
    True
    """

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, model: str = DEFAULT_MODEL, api_key: str | None = None) -> None:
        self.model = model
        self._client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])

    def ask(self, question: str, domain: str = "general") -> str:
        """Send a biology question and return the full response.

        Parameters
        ----------
        question : str
            The user's question in plain English.
        domain : str
            Biology sub-domain for prompt specialisation.
            One of ``"general"``, ``"genomics"``, ``"proteomics"``,
            ``"pathways"``.

        Returns
        -------
        str
            The assistant's response text.

        Raises
        ------
        ValueError
            If *domain* is not a recognised sub-domain.

        Examples
        --------
        >>> client = BiosciClient()
        >>> answer = client.ask("What is a ribosome?")
        >>> len(answer) > 0
        True
        """
        system_prompt = get_system_prompt(domain)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content

    def stream(self, question: str, domain: str = "general") -> Iterator[str]:
        """Stream a biology answer token by token.

        Parameters
        ----------
        question : str
            The user's question.
        domain : str
            Biology sub-domain (see :meth:`ask`).

        Yields
        ------
        str
            Successive text chunks from the model.

        Examples
        --------
        >>> client = BiosciClient()
        >>> chunks = list(client.stream("What is DNA?"))
        >>> len(chunks) > 0
        True
        """
        system_prompt = get_system_prompt(domain)
        stream = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
