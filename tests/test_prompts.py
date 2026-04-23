"""Tests for biosci_chat.prompts module."""

from __future__ import annotations

import pytest

from biosci_chat.prompts import VALID_DOMAINS, get_system_prompt, list_domains


@pytest.mark.parametrize("domain", ["general", "genomics", "proteomics", "pathways"])
def test_get_system_prompt_returns_nonempty_string(domain):
    """get_system_prompt returns a non-empty string for every valid domain."""
    result = get_system_prompt(domain)
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.parametrize("domain", ["general", "genomics", "proteomics", "pathways"])
def test_get_system_prompt_content_is_domain_specific(domain):
    """Each domain returns a distinct prompt string."""
    prompts = {d: get_system_prompt(d) for d in ["general", "genomics", "proteomics", "pathways"]}
    # All prompts must be unique
    assert len(set(prompts.values())) == 4


def test_get_system_prompt_raises_for_unknown_domain():
    """get_system_prompt raises ValueError for an unrecognised domain."""
    with pytest.raises(ValueError):
        get_system_prompt("astrology")


def test_valueerror_message_contains_invalid_domain():
    """The ValueError message includes the invalid domain name."""
    with pytest.raises(ValueError, match="unknown_domain"):
        get_system_prompt("unknown_domain")


def test_valueerror_message_lists_valid_domains():
    """The ValueError message lists the valid domain names."""
    with pytest.raises(ValueError, match="general"):
        get_system_prompt("bad")


def test_list_domains_returns_sorted_list():
    """list_domains returns a sorted list of strings."""
    domains = list_domains()
    assert domains == sorted(domains)


def test_list_domains_contains_all_expected():
    """list_domains contains exactly the four expected domains."""
    assert set(list_domains()) == {"general", "genomics", "proteomics", "pathways"}


def test_list_domains_returns_list_type():
    """list_domains returns a list, not a frozenset or tuple."""
    assert isinstance(list_domains(), list)


def test_valid_domains_is_frozenset():
    """VALID_DOMAINS is a frozenset (immutable)."""
    assert isinstance(VALID_DOMAINS, frozenset)


def test_valid_domains_matches_list_domains():
    """VALID_DOMAINS and list_domains() contain the same elements."""
    assert set(list_domains()) == VALID_DOMAINS
