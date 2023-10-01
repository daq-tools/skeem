.. highlight:: sh


###########
Skeem notes
###########


OKFN and friends
================
- https://github.com/rufuspollock/csv2sqlite
- https://okfnlabs.org/dataconverters/
- https://github.com/okfn/messytables/
- https://github.com/frictionlessdata/tabulator-py


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
- https://dataprotocols.org/ndjson/
- https://agate.readthedocs.io/en/latest/cookbook/create.html#override-type-inference
- https://github.com/peak/s5cmd


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


Outlook
=======
- Tanker is a Python database library targeting analytic operations
  https://github.com/bertrandchenal/tanker
- An implementation of the JSON Schema specification for Python
  https://github.com/python-jsonschema/jsonschema





Parquet
=======

The ``basic.parquet`` file has been created using this code snippet::

    # pip install "pandas<1.6" "pyarrow<12"
    df: pd.DataFrame = pd.read_csv("tests/testdata/basic.csv")
    df = df.set_index("id")
    df["date"] = df["date"].astype("datetime64")
    df.to_parquet("tests/testdata/basic.parquet")

The ``basic.parquet`` file can be explored using the ``parquet-tools`` program like::

    parquet-tools schema tests/testdata/basic.parquet
    parquet-tools dump tests/testdata/basic.parquet


InfluxDB line protocol
======================
- https://docs.influxdata.com/influxdb/cloud/reference/syntax/line-protocol/
- https://github.com/influxdata/line-protocol
- https://github.com/influxdata/line-protocol/blob/v2/lineprotocol/testdata/corpus.json
- https://github.com/influxdata/line-protocol-corpus


InfluxDB docs at Alibaba
========================
- https://www.alibabacloud.com/help/en/time-series-database/latest/line-protocol-reference
- https://www.alibabacloud.com/help/en/time-series-database/latest/line-protocol-tutorial
- https://www.alibabacloud.com/help/en/time-series-database/latest/tsdb-for-influxdb-faq


InfluxDB annotated CSV
======================
- https://docs.influxdata.com/influxdb/latest/reference/syntax/annotated-csv/
- https://docs.influxdata.com/influxdb/latest/reference/syntax/annotated-csv/extended/


Substrait
=========
- https://substrait.io/
- https://github.com/substrait-io/substrait-java
- https://github.com/apache/arrow-datafusion-python/pull/145
- https://github.com/duckdblabs/duckdb-substrait-demo


Misc
====
- https://github.com/toddwschneider/nyc-taxi-data
- https://github.com/taichi-dev/taichi
- Vaex' ``infer_schema``
  https://github.com/vaexio/vaex/blob/652937db59ef099a42ad650cdb19567dcbe1905a/packages/vaex-core/vaex/csv.py#L231-L292
  - https://vaex.io/docs/guides/io.html#Text-based-file-formats
- https://vaex.io/blog/8-incredibly-powerful-Vaex-features-you-might-have-not-known-about
