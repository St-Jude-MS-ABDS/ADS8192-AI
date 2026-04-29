# biosci-chat

[![CI](https://github.com/<username>/biosci-chat/actions/workflows/ci.yml/badge.svg)](https://github.com/<username>/biosci-chat/actions/workflows/ci.yml)
[![Docs](https://github.com/<username>/biosci-chat/actions/workflows/docs.yml/badge.svg)](https://github.com/<username>/biosci-chat/actions/workflows/docs.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/biosci-chat/)

AI-powered biology question answering from the command line.

📖 **[Documentation](https://<username>.github.io/biosci-chat/)**

---

## Overview

`biosci-chat` is a command-line chatbot that answers biology and bioinformatics questions using the OpenAI API. It supports several biology sub-domains with specialised system prompts:

| Domain | Focus |
|--------|-------|
| `general` | General biology questions |
| `genomics` | DNA sequencing, variant calling, genome assembly |
| `proteomics` | Protein structure, mass spectrometry, PTMs |
| `pathways` | Metabolic and signalling pathways |
| `bioinformatics` | Pipelines, formats (FASTA, BAM, VCF), alignment, databases |
| `transcriptomics` | RNA-seq, differential expression, single-cell RNA |
| `microbiology` | Bacteria, viruses, culture, antimicrobial resistance |
| `structural` | Macromolecular structure, cryo-EM, crystallography, PDB |

This project is used as the running example in the **MSABDS AI-Powered Scientific App Development** course module.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<username>/biosci-chat.git
cd biosci-chat

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

## Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-..."   # Windows: set OPENAI_API_KEY=sk-...
```

> **Never commit your API key.** Add `.env` to `.gitignore` and use `python-dotenv` to load it locally.

---

## Usage

### Command-line interface

```bash
# Ask a general biology question (streaming by default)
biosci-chat ask "What is CRISPR-Cas9?"

# Ask with a specific domain
biosci-chat ask "What is a SNP?" --domain genomics

# Disable streaming for non-interactive use
biosci-chat ask "What is a ribosome?" --no-stream

# List available domains
biosci-chat list-domains
```

### Python API

```python
from biosci_chat.client import BiosciClient

client = BiosciClient()

# Single response
answer = client.ask("What is the central dogma of molecular biology?")
print(answer)

# Streaming response
for chunk in client.stream("Explain PCR in simple terms.", domain="genomics"):
    print(chunk, end="", flush=True)
```

---

## Development

### Running tests

```bash
# Run the full test suite with coverage
pytest

# Run a specific test file
pytest tests/test_prompts.py -v

# Run without coverage (faster)
pytest --no-cov
```

### Linting

```bash
ruff check biosci_chat tests
ruff format biosci_chat tests
```

### Building documentation

```bash
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html
```

---

## Project Structure

```
biosci-chat/
├── biosci_chat/
│   ├── __init__.py      ← Package metadata
│   ├── client.py        ← OpenAI API wrapper (BiosciClient)
│   ├── prompts.py       ← System prompt templates
│   └── cli.py           ← Click CLI entry point
├── tests/
│   ├── conftest.py      ← Shared fixtures (mock OpenAI client)
│   ├── test_client.py   ← Tests for BiosciClient
│   ├── test_prompts.py  ← Tests for prompt functions
│   └── test_cli.py      ← Tests for CLI commands
├── docs/
│   ├── conf.py          ← Sphinx configuration
│   ├── index.rst        ← Documentation home
│   ├── api.rst          ← Auto-generated API reference
│   ├── getting_started.rst
│   └── reproducibility.rst
├── .github/workflows/
│   ├── ci.yml           ← Test + lint on push/PR
│   └── docs.yml         ← Deploy docs to GitHub Pages
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

---

## License

MIT License.
