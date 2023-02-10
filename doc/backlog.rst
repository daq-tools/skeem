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
- [x] More type annotations
- [o] eskema infer-ddl --list-input-formats
- [o] Add "examples" to test suite
- [o] Handle spreadsheet format/source: Google Sheets

  - CSV on Google Drive: https://drive.google.com/file/d/1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz/view
  - Google Sheets: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/edit
  - Maybe use tabulator-py? https://github.com/frictionlessdata/tabulator-py#gsheet-read-only

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

- [o] Unlock more input data formats from ``data_dispenser.sources``, like Excel, XML, HTML, MongoDB
- [o] Use https://github.com/frictionlessdata/tabulator-py
- [o] Handle "empty" input
- [o] Process multiple items
- [o] Read archive files

  - https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz

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
  - Spreadsheet formats: Microsoft pendant to Google Sheets, and friends
  - Tables from PDF and others

- [o] pandas Dataframes
- [o] Avro
- [o] JSON Schema
- [o] XML?

- [o] Content type detection using ``python-magic`` and/or ``identify``
- [o] Add Mypy?
