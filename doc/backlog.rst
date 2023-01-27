##############
Eskema backlog
##############


***********
Iteration I
***********

- [x] Add test framework
- [x] Add to repository on GitHub
- [x] Add logging. Use ``--verbose``
- [x] Improve tests
- [x] CLI
- [x] Handle ndjson
- [x] Read from stdin
- [x] Primary key detection
- [x] Slight refactoring
- [x] More OO
- [/] assert_sql_equal
- [x] Remedy magic numbers
- [x] Content type detection using file extension or ``--content-type`` option
- [x] Naming things
- [o] Handle "empty input"
- [o] Handle CSV
- [o] Handle JSON
- [o] CI/GHA
- [o] Docker build & publish
- [o] Docs: Add "other projects"
- [o] File headers
- [o] Release


************
Iteration II
************

- [o] Process multiple items
- [o] Read archive files
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
