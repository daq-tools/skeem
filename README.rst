.. highlight:: sh


######
Eskema
######


*****
About
*****

Infer SQL DDL statements from tabular data, based on the excellent
`SQLAlchemy`_ and `ddlgenerator`_.

Supported input data:

- `NDJSON`_ (formerly LDJSON) aka. `JSON Lines`_, see also `JSON streaming`_
- `CSV`_


********
Synopsis
********

Read data from given file::

    eskema infer-ddl --dialect=postgresql data.ndjson
    eskema infer-ddl --dialect=postgresql data.csv

Reading data from stdin needs to obtain both the table name and content type separately::

    eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson - < data.ndjson
    eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv - < data.csv

Reading data from stdin also works like this, if you prefer to use pipes::

    cat data.ndjson | eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson -
    cat data.csv | eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv -


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
- `Catherine Devlin`_ for `ddlgenerator`_ and `data_dispenser`_.
- All the other countless authors of excellent Python packages,
  Python itself, and turtles all the way down.


.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values
.. _data_dispenser: https://pypi.org/project/data_dispenser/
.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _Catherine Devlin: https://github.com/catherinedevlin
.. _JSON: https://www.json.org/
.. _JSON streaming: https://en.wikipedia.org/wiki/JSON_streaming
.. _JSON Lines: https://jsonlines.org/
.. _Mike Bayer: https://github.com/zzzeek
.. _NDJSON: http://ndjson.org/
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
