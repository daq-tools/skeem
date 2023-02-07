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
- [x] More type annotations

Documentation
=============

- [x] Inline code comments
- [x] Add "other projects" section
- [x] Document library use
- [x] Add example program
- [o] File headers

Infrastructure
==============

- [o] CI/GHA
- [o] Docker build & publish
- [o] Docs: RTD
- [o] Release 0.1.0


***********
Iteration 3
***********

- [o] Unlock more input data formats from ``data_dispenser.sources``, like Excel, XML, HTML, MongoDB
- [o] Handle "empty" input
- [o] Process multiple items
- [o] Read archive files
- [o] Handle JSON and NDJSON with nested objects: ``OBJECT`` and ``ARRAY``
- [o] Support more data types, like ``BOOLEAN``, ``GEO_*``, ``BIT``, ``IP``
- [o] Improve type inference.
  See https://github.com/frictionlessdata/tableschema-py#working-with-table


***********
Iteration 4
***********

- [o] HTTP API endpoint
- [o] Add more input formats

  - InfluxDB line protocol
  - Parquet and friends
  - Fixed-width, using ``pd.read_fwf()``
  - XLSX, ODF, and other spreadsheets like Google Sheets, its Microsoft pendant, and friends
  - pandas Dataframes
  - Avro
  - JSON Schema
  - XML?

- [o] Content type detection using ``python-magic`` and/or ``identify``
- [o] Add Mypy?
