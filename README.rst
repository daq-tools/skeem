.. highlight:: sh


######
Eskema
######


*****
About
*****

Infer SQL DDL statements from tabular data, based on the excellent
`SQLAlchemy`_ and `ddlgenerator`_.

Supported input data: `ndjson`_ aka. `JSON Lines`_.


********
Synopsis
********

Read data from given file::

    eskema infer-ddl --dialect=postgresql data.ndjson

Reading data from stdin needs to obtain the table name separately::

    eskema infer-ddl --dialect=crate --table-name=foo - < data.ndjson
    cat data.ndjson | eskema infer-ddl --dialect=crate --table-name=foo -


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


.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values
.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _Catherine Devlin: https://github.com/catherinedevlin
.. _JSON: https://www.json.org/
.. _JSON Lines: https://jsonlines.org/
.. _Mike Bayer: https://github.com/zzzeek
.. _ndjson: http://ndjson.org/
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
