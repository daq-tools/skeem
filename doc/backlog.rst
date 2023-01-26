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
- [o] Content type detection using file extension
- [o] Handle JSON
- [o] Handle CSV
- [o] Slight refactoring
- [o] CI/GHA
- [o] More OO
- [o] Docker build & publish
- [o] Docs: Add "other projects"
- [o] Release


************
Iteration II
************

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
