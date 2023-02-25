##############
Eskema backlog
##############


***********
Iteration 1
***********

- [x] Add test framework
- [x] Add to repository on GitHub
- [x] Add logging. Use ``--verbose``
- [x] Improve tests
- [x] CLI
- [x] Handle NDJSON
- [x] Read from stdin
- [x] Primary key detection
- [x] Slight refactoring
- [x] More OO
- [/] assert_sql_equal
- [x] Remedy magic numbers
- [x] Content type detection using file extension or ``--content-type`` option
- [x] Naming things


***********
Iteration 2
***********

Features
========

- [x] Handle CSV
- [x] Handle basic JSON: records + single document
- [x] Handle spreadsheet formats: XLSX and ODF
- [x] Add more type annotations, and `mypy`_
- [x] Add `frictionless`_ backend
- [x] Add software tests for `frictionless`_ backend
- [x] Add support for Google Sheets input format
- [x] Add support for Parquet input format
- [x] Support reading large files efficiently
- [x] Support reading data from HTTP
- [x] Bug: Why is resource being read twice?
- [o] Refactor more code to ``eskema.io``
- [o] Add support for "InfluxDB line protocol" input format
- [o] Support reading large files from HTTP efficiently
- [o] Support reading data from HTTP, without file suffix, and/or query parameters
- [o] Support reading data from S3
- [o] Enable ``frictionless`` backend using environment variable ``ESKEMA_BACKEND=frictionless``
- [o] Add help texts to CLI options
- [o] eskema infer-ddl --list-input-formats
- [o] Add "examples" to test suite
- [o] Provide options to control sample size
- [o] Is table- and field-name quoting properly applied for both backends?
- [o] API/Docs: Derive schema directly from pandas DataFrame

Documentation
=============

- [x] Inline code comments
- [x] Add "other projects" section
- [x] Document library use
- [x] Add example program
- [/] File headers
- [o] Improve "library use" docs re. ``ContentType``
- [o] Read data from Sensor.Community archive
- [o] Read data from IP to Country database

  - https://db-ip.com/db/format/ip-to-city-lite/csv.html
  - http://download.db-ip.com/free/dbip-city-lite-2023-02.csv.gz

Infrastructure
==============

- [o] CI/GHA
- [o] Docker build & publish
- [o] Docs: RTD
- [o] Release 0.1.0
- [o] Issue: Hello world

Quality
=======
- [o] QA: Use reference input test data from other repositories

  - https://github.com/okfn/messytables/tree/master/horror
  - https://github.com/frictionlessdata/tabulator-py/tree/main/data/special
  - https://github.com/apache/arrow-testing/tree/master/data
  - https://github.com/pandas-dev/pandas/tree/main/doc/data


***********
Iteration 3
***********

- [o] Use ``smart_open``
  https://github.com/RaRe-Technologies/smart_open
- [o] Support reading archive files directly. Examples:

  - https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz
- [o] Add support for Google Drive input source
  https://drive.google.com/file/d/1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz/view
- [o] Unlock more input data formats from ``data_dispenser.sources``, like Excel, XML, HTML, MongoDB
- [o] Handle "empty" input
- [o] Process multiple items
- [o] CrateDB: Handle JSON and NDJSON with nested objects: ``OBJECT`` and ``ARRAY``
- [o] CrateDB: Support more data types, like ``BOOLEAN``, ``GEO_*``, ``BIT``, ``IP``
- [o] Improve type inference.
  See https://github.com/frictionlessdata/tableschema-py#working-with-table
- [o] Optimize ``fastparquet.core.read_col``: ``infile.read(cmd.total_compressed_size)``
- [o] Can Parquet header (and types) be inquired without needing to read actual data?
- [o] Add ``pandas`` backend


Bugs
====
- [o] ``HTTP/1.1 403 Forbidden`` gets masked badly
- [o] Fix ``cat foo | --backend=fl -``
- [o] ``logger.warning`` will emit to STDOUT when running per tests


***********
Iteration 4
***********

- [o] HTTP API endpoint
- [o] Add more input formats and sources

  - Parquet and friends
  - Fixed-width, using ``pd.read_fwf()``
  - pandas Dataframes
  - Avro
  - JSON Schema
  - XML, RDF, RSS
    https://data.cityofnewyork.us/Transportation/2017-Yellow-Taxi-Trip-Data/biws-g3hs
  - Spreadsheet formats: Microsoft pendant to Google Sheets, and friends
  - Tables from PDF and others
  - DuckDB can currently directly run queries on Parquet files, CSV files,
    SQLite files, Pandas, R and Julia data frames as well as Apache Arrow
    sources. This new extension adds the capability to directly query
    PostgreSQL tables from DuckDB.
    -- https://duckdb.org/2022/09/30/postgres-scanner.html

- [o] Content type detection using ``python-magic`` and/or ``identify``
- [o] Text-to-SQL

  - https://github.com/paulfitz/mlsql
  - https://github.com/Microsoft/rat-sql

- [o] Support for Grist

  - https://github.com/gristlabs/grist-core
  - https://docs.getgrist.com/doc/new~vhzPQwVDmAKY5nJXcGvcH7
  - https://paulfitz.github.io/2020/08/01/translate-english-to-sql-progress-updates.html

- [o] Discover: Scan filesystem folder (and files within archives) for matching file types
- [o] What about ``datatable``, with a "specific emphasis on speed and big data support"?
  https://github.com/h2oai/datatable

- [o] Make option ``--address="Sheet2"`` work for Google Sheets
- [o] Inquire schema data from out-of-band channel. For example,
  https://data.cityofnewyork.us/resource/biws-g3hs.csv::

    X-SODA2-Data-Out-Of-Date: false
    X-SODA2-Fields: ["vendorid","tpep_pickup_datetime","tpep_dropoff_datetime","passenger_count","trip_distance","ratecodeid","store_and_fwd_flag","pulocationid","dolocationid","payment_type","fare_amount","extra","mta_tax","tip_amount","tolls_amount","improvement_surcharge","total_amount"]
    X-SODA2-Secondary-Last-Modified: Thu, 13 Sep 2018 21:32:08 GMT
    X-SODA2-Truth-Last-Modified: Thu, 13 Sep 2018 21:32:08 GMT
    X-SODA2-Types: ["number","floating_timestamp","floating_timestamp","number","number","number","text","number","number","number","number","number","number","number","number","number","number"]


.. _frictionless: https://github.com/frictionlessdata/framework
.. _mypy: https://pypi.org/project/mypy/
