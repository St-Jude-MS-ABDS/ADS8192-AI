# Testing Guide

## What is Tested and Why

`biosci-chat` uses a layered testing strategy:

| Layer | Files | Why |
|-------|-------|-----|
| Unit | `test_prompts.py`, `test_client.py` | Validate logic in isolation; fast and free |
| Integration | `test_cli.py` | Verify CLI commands produce correct output |
| E2E | Manual / nightly | Real API calls; costs money, non-deterministic |

The OpenAI API is **always mocked** in automated tests using the `mock_client`
fixture in `conftest.py`. This ensures tests are fast, free, and deterministic.

## Running Tests Locally

```bash
# Full suite with coverage report
pytest

# Specific file
pytest tests/test_prompts.py -v

# Skip coverage (faster)
pytest --no-cov

# Show only failures
pytest -x
```

## Interpreting Coverage Reports

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
biosci_chat/__init__.py         3      0   100%
biosci_chat/client.py          28      2    93%   45, 52
biosci_chat/cli.py             22      4    82%   38-41
biosci_chat/prompts.py         14      0   100%
---------------------------------------------------------
TOTAL                          67      6    91%
```

- **Stmts**: Total executable statements
- **Miss**: Statements not executed by any test
- **Cover**: Percentage covered
- **Missing**: Line numbers not covered — investigate these

The CI pipeline fails if total coverage drops below **80%**.

## CI Matrix

Tests run on 9 combinations: 3 operating systems × 3 Python versions.

| OS | Python 3.10 | Python 3.11 | Python 3.12 |
|----|-------------|-------------|-------------|
| ubuntu-latest | ✓ | ✓ (+ coverage upload) | ✓ |
| macos-latest | ✓ | ✓ | ✓ |
| windows-latest | ✓ | ✓ | ✓ |

Cross-platform failures typically indicate path separator issues, line ending
differences, or case-sensitivity problems. Use `pathlib.Path` for all file
paths to avoid platform-specific bugs.

## Adding Tests for New Features

1. Create `tests/test_<module>.py` for new modules
2. Use `mock_client` fixture for anything that touches `BiosciClient`
3. Use `CliRunner` from `click.testing` for CLI tests
4. Add `@pytest.mark.parametrize` for functions with multiple valid inputs
5. Run `pytest --cov` locally and confirm coverage stays ≥ 80%
