.. highlight:: sh


############
Eskema notes
############


The early days
==============
- https://github.com/rufuspollock/csv2sqlite
- http://okfnlabs.org/dataconverters/
- https://github.com/okfn/messytables/


Converting arbitrary nested json to CSV?
========================================
- https://github.com/wireservice/csvkit/issues/653
- https://github.com/konklone/json/issues/95
- https://github.com/konklone/json/issues/90


Konkline - A free, in-browser JSON to CSV converter
===================================================
- https://github.com/konklone/json
- https://konklone.io/json/

Misc
====
- https://towardsdatascience.com/automatically-inferring-relational-structure-from-files-ee0790c8002c
- https://pypi.org/project/csv-schema-inference/
- https://stackoverflow.com/questions/69874809/how-can-i-infer-the-candidate-key-from-csv-files
- https://stackabuse.com/python-how-to-flatten-list-of-lists/
- https://github.com/ndjson/ndjson.github.io/issues/1
- https://agate.readthedocs.io/en/latest/cookbook/create.html#override-type-inference

csvkit
======
::

    pip install csvkit
    export CSVFILE=tests/testdata/basic.csv
    csvsql --dialect sqlite "${CSVFILE}"
    csvsql --dialect crate "${CSVFILE}"
    csvsql --dialect postgresql "${CSVFILE}"

    # What about `--date-format='%s'`?

::

    csvsql -v --dialect=crate --db-schema=testdrive "${CSVFILE}"

.. code-block:: sql

    CREATE TABLE testdrive.basic (
        id FLOAT NOT NULL,
        name VARCHAR NOT NULL,
        date VARCHAR NOT NULL,
        fruits VARCHAR NOT NULL,
        price BOOLEAN
    );

