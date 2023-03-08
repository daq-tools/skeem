###########
Development
###########


*******
Sandbox
*******

Acquire sources, create Python virtualenv, install package and dependencies,
and run software tests::

    git clone https://github.com/daq-tools/skeem
    cd skeem
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.[test,develop,release,scientific]

    # Run regular test suite.
    poe test

    # Run "roadrunner" tests, using a bunch of external resources. The tests will
    # only check for a successful invocation, and not verify the generated SQL.
    poe test-roadrunner


************
Code tracing
************

Skeem uses `Hunter`_ for code tracing, in order to make it easy to identify
hot spots visually. `Hunter`_ is a flexible code tracing toolkit, for
debugging, logging, inspection and other nefarious purposes.

For tracing function invocations through ``skeem`` and important 3rd-party
modules, use the ``--trace-modules=`` option. Examples:

- ``--trace-modules=frictionless`` will trace code execution for the
  ``frictionless`` module.
- ``--trace-modules=skeem,frictionless, pandas`` will trace code execution for
  the ``skeem``, ``frictionless``, and ``pandas`` modules.
- ``--trace-modules=machinery`` has a special meaning, and will resolve to the
  module list ``["skeem", "fastparquet", "frictionless", "fsspec", "pandas"]``.


.. _Hunter: https://pypi.org/project/hunter/
