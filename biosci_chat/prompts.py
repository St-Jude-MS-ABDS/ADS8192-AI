"""System prompt templates for different biology sub-domains."""

from __future__ import annotations

_PROMPTS: dict[str, str] = {
    "general": (
        "You are a knowledgeable biology assistant. "
        "Answer questions accurately and concisely, citing sources where possible. "
        "If you are unsure, say so explicitly rather than guessing."
    ),
    "genomics": (
        "You are an expert genomics assistant specialising in DNA sequencing, "
        "variant calling, and genome assembly. Use standard nomenclature (HGVS, "
        "Ensembl gene IDs) and cite primary literature when relevant."
    ),
    "proteomics": (
        "You are a proteomics expert. Answer questions about protein structure, "
        "function, mass spectrometry, and post-translational modifications. "
        "Reference UniProt accessions where appropriate."
    ),
    "pathways": (
        "You are a systems biology assistant focused on metabolic and signalling "
        "pathways. Reference KEGG or Reactome pathway IDs when relevant."
    ),
}

VALID_DOMAINS = frozenset(_PROMPTS)


def get_system_prompt(domain: str = "general") -> str:
    """Return the system prompt for a given biology sub-domain.

    Parameters
    ----------
    domain : str
        One of ``"general"``, ``"genomics"``, ``"proteomics"``, ``"pathways"``.

    Returns
    -------
    str
        The system prompt string.

    Raises
    ------
    ValueError
        If *domain* is not recognised.

    Examples
    --------
    >>> get_system_prompt("general")
    'You are a knowledgeable biology assistant...'
    >>> get_system_prompt("invalid")
    Traceback (most recent call last):
        ...
    ValueError: Unknown domain 'invalid'. Valid domains: ['general', 'genomics', 'pathways', 'proteomics']
    """
    if domain not in _PROMPTS:
        raise ValueError(
            f"Unknown domain {domain!r}. Valid domains: {sorted(VALID_DOMAINS)}"
        )
    return _PROMPTS[domain]


def list_domains() -> list[str]:
    """Return a sorted list of available biology sub-domains.

    Returns
    -------
    list of str
        Sorted list of domain names.

    Examples
    --------
    >>> list_domains()
    ['general', 'genomics', 'pathways', 'proteomics']
    """
    return sorted(VALID_DOMAINS)
