######
Eskema
######


*****
About
*****

Infer SQL DDL statements from tabular data, based on the excellent
`ddlgenerator`_.

Supported input data: `JSON`_, `ndjson`_.


********
Synopsis
********
::

    eskema infer-ddl --dialect=postgresql data.ndjson


***********
Development
***********

Acquire sources, create Python virtualenv, install package and dependencies,
and run software tests::

    git clone https://github.com/daq-tools/eskema
    cd eskema
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.[test,develop,release]
    poe test


*******
Credits
*******

- `Mike Bayer`_ for `SQLAlchemy`_.
- `Catherine Devlin`_ for `ddlgenerator`_.
- All the other countless authors of excellent Python packages,
  Python itself, and turtles all the way down.


.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _Catherine Devlin: https://github.com/catherinedevlin
.. _JSON: https://www.json.org/
.. _Mike Bayer: https://github.com/zzzeek
.. _ndjson: http://ndjson.org/
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
