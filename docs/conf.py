"""Sphinx configuration for biosci-chat documentation."""

from __future__ import annotations

import sys
from pathlib import Path

# Make the biosci_chat package importable during the doc build
sys.path.insert(0, str(Path(__file__).parent.parent))

# -- Project information -------------------------------------------------------
project = "biosci-chat"
copyright = "2024, Your Name"
author = "Your Name"
release = "0.1.0"

# -- General configuration -----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc -------------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "special-members": "__init__",
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# -- Napoleon (NumPy docstring style) ------------------------------------------
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_rtype = False

# -- Intersphinx ---------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- HTML output ---------------------------------------------------------------
html_theme = "furo"
html_title = "biosci-chat"
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}
html_static_path = ["_static"]
