# Changelog

All notable changes to biosci-chat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-03-01

### Added

- `BiosciClient` class with `ask()` and `stream()` methods
- Four biology sub-domains: `general`, `genomics`, `proteomics`, `pathways`
- Domain-specific system prompt templates in `prompts.py`
- Click CLI with `ask` and `list-domains` commands
- pytest test suite with mock OpenAI client fixtures (≥80% coverage)
- Sphinx documentation site with API reference and getting-started guide
- GitHub Actions CI workflow (ubuntu/macos/windows × Python 3.10/3.11/3.12)
- Automated docs deployment to GitHub Pages
- NumPy-style docstrings for all public API
