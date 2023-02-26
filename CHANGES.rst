################
Eskema changelog
################


in progress
===========

- Initial working version, supporting JSON
- Add CLI subsystem
- Add logging
- Add SQL pretty printing
- Improve software tests
- Unlock reading from stdin
- Derive table name from input file name
- Primary key detection
- Content type detection using file extension or ``--content-type`` option
- Add support for CSV input format
- Add support for XLSX and ODS input formats
- Add test case for basic nested JSON document
- Add ``frictionless`` backend
- Add support for Google Sheets and Parquet input formats
- Improve sampling large files
- Support reading data from HTTP
- Performance: Use the Hunter code tracing toolkit to trace execution path
- Performance: Don't open resource twice when using ``frictionless`` backend
- Performance: Improve peeking into Parquet files
- Performance: Configure ``PEEK_LINES = 100`` instead of 1000
- Performance: Optimize reading from remote NDJSON files
- Refactoring: I/O related code goes into ``eskema.io``
- Add support for InfluxDB line protocol input format
- Source: Unlock reading from public S3 buckets anonymously (``--no-sign-request``)
- Source: Unlock and document reading from public Google Cloud Storage (GCS) buckets,
  and files on GitHub.
- Tests: Add "roadrunner" tests, using a bunch of external resources. The tests
  will only check for successful invocation, and not verify the generated SQL.
- Format: Add NetCDF input format


2023-01-xx 0.0.0
================
