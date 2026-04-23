Getting Started
===============

This guide takes you from zero to running your first biology query in under
10 minutes.

Installation
------------

.. code-block:: bash

   git clone https://github.com/<username>/biosci-chat.git
   cd biosci-chat
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"

Setting Your API Key
--------------------

``biosci-chat`` requires an OpenAI API key. Set it as an environment variable:

.. code-block:: bash

   export OPENAI_API_KEY="sk-..."   # macOS/Linux
   set OPENAI_API_KEY=sk-...        # Windows CMD

.. note::
   Never commit your API key to version control. Add ``.env`` to
   ``.gitignore`` and use ``python-dotenv`` to load it locally.

Your First Query
----------------

.. code-block:: bash

   # Ask a general biology question
   biosci-chat ask "What is CRISPR-Cas9?"

   # Ask with a specific domain
   biosci-chat ask "What is a SNP?" --domain genomics

   # List available domains
   biosci-chat list-domains

Using the Python API
--------------------

.. code-block:: python

   from biosci_chat.client import BiosciClient

   client = BiosciClient()

   # Single response
   answer = client.ask("What is the central dogma?")
   print(answer)

   # Streaming response
   for chunk in client.stream("Explain PCR.", domain="genomics"):
       print(chunk, end="", flush=True)

Choosing a Domain
-----------------

Use the ``--domain`` flag (CLI) or ``domain`` parameter (Python API) to
specialise the response:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Domain
     - Best for
   * - ``general``
     - Broad biology questions, cell biology, evolution
   * - ``genomics``
     - DNA sequencing, variant calling, genome assembly
   * - ``proteomics``
     - Protein structure, mass spectrometry, PTMs
   * - ``pathways``
     - Metabolic and signalling pathways (KEGG, Reactome)

Troubleshooting
---------------

**KeyError: 'OPENAI_API_KEY'**
   The environment variable is not set. Run
   ``export OPENAI_API_KEY="sk-..."`` before using the CLI.

**openai.AuthenticationError**
   Your API key is invalid or has expired. Check
   `platform.openai.com <https://platform.openai.com>`_ for a valid key.

**ValueError: Unknown domain**
   The domain name is misspelled. Run ``biosci-chat list-domains`` to see
   valid options.
