.. highlight:: sh


############
Eskema notes
############


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


Online spreadsheets
===================


- Google Drive at ``drive.google.com`` or ``docs.google.com``:

  - | https://docs.google.com/file/d/1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz/view
    | ``http "https://drive.google.com/uc?export=download&id=1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz" --follow``

- Google Sheets:

  - VES:

    - basic: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/edit
    - Sheet2: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/edit#gid=883324548
  - CSV:

    - basic: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=csv
    - Sheet2: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?gid=883324548&format=csv
  - XLSX: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=xlsx
  - ODS: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=ods
  - More formats: tsv, zip, pdf

- Google AppSheet App:

  - https://www.appsheet.com/Template/AppDef?appName=basic-285352295&appId=f6f7024c-5ab6-46c1-863b-c446eb2f4c28&channel=gdrive
  - Table editor: https://www.appsheet.com/Template/AppDef?appName=basic-285352295#Data.Tables.basic
  - Table view: https://www.appsheet.com/template/showtable?appId=basic-285352295&tableName=basic
  - Share » Editor: https://www.appsheet.com/Template/AppDef?appName=basic-285352295&utm_source=share_app_link
  - Share » Browser: https://www.appsheet.com/start/f6f7024c-5ab6-46c1-863b-c446eb2f4c28
  - Share » Install: https://www.appsheet.com/newshortcut/f6f7024c-5ab6-46c1-863b-c446eb2f4c28
  - Report » Looker Studio: https://lookerstudio.google.com/reporting/create?c.mode=edit&c.reportId=8225cc90-e702-42a1-9d9b-4aca626f6d1e&c.explain=true&ds.connector=COMMUNITY&ds.deploymentId=AKfycbxy0_bVIUsKVRWtvA0fJfEq_F_wdP2whFOQGskykubSizkpmQojrOFMe1EN9rz6klk0&ds.appId=f6f7024c-5ab6-46c1-863b-c446eb2f4c28&ds.tableName=basic&ds.refreshFields=true&plugin.id=AppSheet&plugin.report=%7B%20%22v1%22:%20%7B%20%22t%22:%20%22basic:%20basic%22,%20%22c%22:%20%7B%20%7D,%20%22b%22:%20%7B%20%22t%22:%20%7B%20%22d%22:%20%5B%20%22name%22,%20%22date%22,%20%22fruits%22%20%5D,%20%22m%22:%20%5B%20%7B%20%22d%22:%20%22price%22,%20%22a%22:%20%22METRIC_AGGREGATION_MAX%22%20%7D%20%5D%20%7D%20%7D%20%7D%20%7D

- AppSheet database, table »basic«:

  - Edit: https://www.appsheet.com/dbs/database/sqnDBz26zA4gU-gNcB8eZa/table/EmXXq1RtFn4a2elXmJ3Le4
  - Share: https://www.appsheet.com/dbs/database/sqnDBz26zA4gU-gNcB8eZa

- TODO: Google AppSheet » New table » New source » On-premises database » Add DreamFactory connection » Postgres

  - https://www.appsheet.com/Account/DreamFactoryAuthInfo?state=e2a33e28-9026-46d8-8230-93c36fbc837d
  - https://www.dreamfactory.com/


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


ILP example data
================
- https://github.com/influxdata/influxdb2-sample-data

Small files:
- https://github.com/Anaisdg/GettingStarted_WritingPoints/blob/master/Data/chronograf.txt

Large files:
- https://github.com/Anaisdg/GettingStarted_WritingPoints/blob/master/Data/import.txt


InfluxDB docs at Alibaba
========================
- https://www.alibabacloud.com/help/en/time-series-database/latest/line-protocol-reference
- https://www.alibabacloud.com/help/en/time-series-database/latest/line-protocol-tutorial
- https://www.alibabacloud.com/help/en/time-series-database/latest/tsdb-for-influxdb-faq
