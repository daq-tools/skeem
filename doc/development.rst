###########
Development
###########

Acquire sources, create Python virtualenv, install package and dependencies,
and run software tests::

    git clone https://github.com/daq-tools/eskema
    cd eskema
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.[test,develop,release]
    poe test

