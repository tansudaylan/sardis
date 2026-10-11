Getting started
===============

Installation
------------

Install Sardis from its repository root:

.. code-block:: console

   python -m pip install -e .

Set ``SARDIS_PATH`` to the repository root for workflows that read local inputs
or save generated products.

Synthetic vetting example
-------------------------

The maintained example passes a seeded synthetic target population through
Sardis and plots classification performance:

.. code-block:: console

   python examples/synthetic_vetting_performance.py --typefileplot png

The example uses generated labels and targets; it does not report observed TESS
candidate performance or survey occurrence.