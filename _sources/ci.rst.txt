Continuous Integration
======================

``biosci-chat`` uses GitHub Actions for automated testing, linting, and
documentation deployment.

Workflows
---------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Workflow
     - Trigger
     - What it does
   * - ``ci.yml``
     - Push to main, any PR
     - Tests on 3 OS × 3 Python versions, lints with ruff, uploads coverage
   * - ``docs.yml``
     - Push to main
     - Builds Sphinx docs and deploys to GitHub Pages
   * - ``release.yml``
     - Push of a ``v*`` tag
     - Builds and publishes the package to PyPI

Running Tests Locally
---------------------

.. code-block:: bash

   # Install development dependencies
   pip install -e ".[dev]"

   # Run the full test suite with coverage
   pytest

   # Run only a specific test file
   pytest tests/test_prompts.py -v

   # Run without coverage (faster)
   pytest --no-cov

Linting
-------

.. code-block:: bash

   # Check for linting errors
   ruff check biosci_chat tests

   # Auto-fix fixable issues
   ruff check --fix biosci_chat tests

   # Check formatting
   ruff format --check biosci_chat tests

   # Apply formatting
   ruff format biosci_chat tests

Coverage Requirements
---------------------

The CI pipeline requires ≥ 80% test coverage. Run the coverage report
locally before pushing:

.. code-block:: bash

   pytest --cov=biosci_chat --cov-report=term-missing
   # Check the TOTAL line — it must be ≥ 80%

Adding New Tests
----------------

Place new test files in the ``tests/`` directory with the naming convention
``test_<module>.py``. Use the fixtures in ``conftest.py`` to avoid making
real API calls.
