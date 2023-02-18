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
- [o] Support reading data from HTTP, without file suffix
- [o] Support reading large files from HTTP efficiently
- [o] Support reading data from S3
- [o] Enable ``frictionless`` backend using environment variable ``ESKEMA_BACKEND=frictionless``
- [o] Add help texts to CLI options
- [o] eskema infer-ddl --list-input-formats
- [o] Add "examples" to test suite
- [o] Control sample size

Documentation
=============

- [x] Inline code comments
- [x] Add "other projects" section
- [x] Document library use
- [x] Add example program
- [/] File headers
- [o] Improve "library use" docs re. ``ContentType``

Infrastructure
==============

- [o] CI/GHA
- [o] Docker build & publish
- [o] Docs: RTD
- [o] Release 0.1.0
- [o] Issue: Hello world
- [o] Issue: Collection of bogus input data

  - https://github.com/okfn/messytables/tree/master/horror
  - https://github.com/frictionlessdata/tabulator-py/tree/main/data/special


***********
Iteration 3
***********

- [o] Support reading archive files directly. Examples:

  - https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz
- [o] Add support for Google Drive input source
  https://drive.google.com/file/d/1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz/view
- [o] Unlock more input data formats from ``data_dispenser.sources``, like Excel, XML, HTML, MongoDB
- [o] Handle "empty" input
- [o] Process multiple items
- [o] Handle JSON and NDJSON with nested objects: ``OBJECT`` and ``ARRAY``
- [o] Support more data types, like ``BOOLEAN``, ``GEO_*``, ``BIT``, ``IP``
- [o] Improve type inference.
  See https://github.com/frictionlessdata/tableschema-py#working-with-table


***********
Iteration 4
***********

- [o] HTTP API endpoint
- [o] Add more input formats and sources

  - InfluxDB line protocol
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


.. _frictionless: https://github.com/frictionlessdata/framework
.. _mypy: https://pypi.org/project/mypy/
