Reproducibility Protocol
========================

This page documents the steps required to reproduce results produced by
``biosci-chat``. Scientific reproducibility requires pinning all sources
of variability: software versions, model versions, and random seeds.

Environment Pinning
-------------------

Always record the exact environment used to produce a result:

.. code-block:: bash

   # Export the full environment
   pip freeze > requirements-lock.txt

   # Record the Python version
   python --version >> requirements-lock.txt

   # Record the biosci-chat version
   python -c "import biosci_chat; print(biosci_chat.__version__)" >> requirements-lock.txt

Model Version Pinning
---------------------

OpenAI model aliases (e.g. ``gpt-4o-mini``) are not stable — the model
behind the alias may change without notice. For reproducible results, use a
dated snapshot:

.. code-block:: python

   # Use a dated model snapshot instead of the alias
   client = BiosciClient(model="gpt-4o-mini-2024-07-18")

.. warning::
   Results from language models are non-deterministic by default. Even with
   the same model and prompt, responses will vary between runs. Set
   ``temperature=0`` for maximum determinism (though identical outputs are
   still not guaranteed).

Temperature Configuration
-------------------------

To minimise response variability, pass ``temperature=0`` via a subclass or
by extending ``BiosciClient``:

.. code-block:: python

   from biosci_chat.client import BiosciClient
   from biosci_chat.prompts import get_system_prompt

   class ReproducibleClient(BiosciClient):
       """BiosciClient with temperature=0 for reproducible outputs."""

       def ask(self, question: str, domain: str = "general") -> str:
           system_prompt = get_system_prompt(domain)
           response = self._client.chat.completions.create(
               model=self.model,
               messages=[
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": question},
               ],
               temperature=0,
           )
           return response.choices[0].message.content

Logging Queries and Responses
------------------------------

For audit trails, log all queries and responses to a JSONL file:

.. code-block:: python

   import json
   from datetime import datetime, timezone
   from pathlib import Path

   from biosci_chat.client import BiosciClient


   class LoggingClient(BiosciClient):
       """BiosciClient that logs all queries and responses to JSONL."""

       def __init__(self, log_path: str = "biosci_chat_log.jsonl", **kwargs):
           super().__init__(**kwargs)
           self._log_path = Path(log_path)

       def ask(self, question: str, domain: str = "general") -> str:
           response = super().ask(question, domain=domain)
           record = {
               "timestamp": datetime.now(timezone.utc).isoformat(),
               "model": self.model,
               "domain": domain,
               "question": question,
               "response": response,
           }
           with self._log_path.open("a") as f:
               f.write(json.dumps(record) + "\n")
           return response

Citing biosci-chat
------------------

If you use ``biosci-chat`` in a publication, cite it as:

.. code-block:: text

   Author, Y. (2024). biosci-chat: AI-powered biology question answering
   (Version 0.1.0) [Software]. GitHub.
   https://github.com/<username>/biosci-chat
