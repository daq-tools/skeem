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
    pip install --use-pep517 --prefer-binary --editable=.[test,develop,release,scientific]

    # Run linter and regular test suite.
    poe check

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


****************
Build OCI images
****************

OCI images will be automatically published to the GitHub Container Registry
(GHCR), see `Skeem packages on GHCR`_. If you want to build images on your
machine, you can use those commands::

    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    export BUILDKIT_PROGRESS=plain
    docker build --tag local/skeem-standard --file release/oci/standard.Dockerfile .
    docker build --tag local/skeem-full --file release/oci/full.Dockerfile .

::

    docker run --rm -it local/skeem-standard skeem --version
    docker run --rm -it local/skeem-standard skeem info


.. _Hunter: https://pypi.org/project/hunter/
.. _Skeem packages on GHCR: https://github.com/orgs/daq-tools/packages?repo_name=skeem
