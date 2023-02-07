.. highlight:: sh


######
Eskema
######


*****
About
*****

Infer SQL DDL statements from tabular data, based on the excellent
`SQLAlchemy`_ and `ddlgenerator`_ packages.

Supported input data:

- `CSV`_
- `JSON`_
- `NDJSON`_ (formerly LDJSON) aka. `JSON Lines`_, see also `JSON streaming`_


********
Synopsis
********

::

    eskema infer-ddl --dialect=postgresql data.ndjson

.. code-block:: sql

    CREATE TABLE "data" (
        "id" SERIAL NOT NULL,
        "name" TEXT NOT NULL,
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "fruits" TEXT NOT NULL,
        "price" DECIMAL(2, 2) NOT NULL,
        PRIMARY KEY ("id")
    );


*****
Usage
*****

Command line use
================

Read data from given file::

    eskema infer-ddl --dialect=postgresql data.ndjson
    eskema infer-ddl --dialect=postgresql data.json
    eskema infer-ddl --dialect=postgresql data.csv

Reading data from stdin needs to obtain both the table name and content type separately::

    eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson - < data.ndjson
    eskema infer-ddl --dialect=crate --table-name=foo --content-type=json - < data.json
    eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv - < data.csv

Reading data from stdin also works like this, if you prefer to use pipes::

    cat data.ndjson | eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson -
    cat data.json | eskema infer-ddl --dialect=crate --table-name=foo --content-type=json -
    cat data.csv | eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv -


Library use
===========

.. code-block:: python

    import io
    from eskema.core import SchemaGenerator
    from eskema.model import Resource, SqlTarget

    INDATA = io.StringIO(
        """
        {"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
        {"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
        """
    )

    sg = SchemaGenerator(
        resource=Resource(data=INDATA, content_type="ndjson"),
        target=SqlTarget(dialect="crate", table_name="testdrive"),
    )

    print(sg.to_sql_ddl().pretty)

.. code-block:: sql

    CREATE TABLE "testdrive" (
        "id" INT NOT NULL,
        "name" STRING NOT NULL,
        "date" TIMESTAMP,
        "fruits" STRING NOT NULL,
        "price" DOUBLE NOT NULL,
        PRIMARY KEY ("id")
    );


***********
Development
***********

For working with the latest development version, please follow the
`development`_ documentation.


*********************
Credits and prior art
*********************

- `Mike Bayer`_ for `SQLAlchemy`_.
- `Catherine Devlin`_ for `ddlgenerator`_ and `data_dispenser`_.
- All the other countless authors of excellent Python packages,
  Python itself, and turtles all the way down.
- More prior art: We are maintaining a `list of other projects`_ with the same
  or similar goals like Eskema.


.. _Catherine Devlin: https://github.com/catherinedevlin
.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values
.. _data_dispenser: https://pypi.org/project/data_dispenser/
.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _development: doc/development.rst
.. _JSON: https://www.json.org/
.. _JSON streaming: https://en.wikipedia.org/wiki/JSON_streaming
.. _JSON Lines: https://jsonlines.org/
.. _list of other projects: doc/prior-art.rst
.. _Mike Bayer: https://github.com/zzzeek
.. _NDJSON: http://ndjson.org/
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
