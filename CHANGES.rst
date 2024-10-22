###############
Skeem changelog
###############


in progress
===========

2024-10-22 v0.1.1
=================
- Added support for Python 3.12 and 3.13
- Adjusted SQL DDL for sqlalchemy-cratedb 0.40.0
- Adjusted ddlgenerator wrapper for pandas 2
- Updated to frictionless >=5.16

2023-03-09 v0.1.0
=================
- Initial working version, supporting JSON
- Add CLI subsystem
- Add logging
- Add SQL pretty printing
- Improve software tests
- Source: Unlock reading from stdin
- Derive table name from input file name
- Primary key detection
- Format: Content type detection using file extension or ``--content-type`` option
- Format: Add support for CSV input format
- Format: Add support for XLSX and ODS input formats
- Tests: Add test case for basic nested JSON document
- Backend: Add ``frictionless`` backend
- Format: Add support for Google Sheets and Parquet input formats
- Performance: Improve sampling large files
- Source: Support reading data from HTTP
- Performance: Use the Hunter code tracing toolkit to trace execution path
- Performance: Don't open resource twice when using ``frictionless`` backend
- Performance: Improve peeking into Parquet files
- Performance: Configure ``PEEK_LINES = 100`` instead of 1000
- Performance: Optimize reading from remote NDJSON files
- Refactoring: I/O related code goes into ``skeem.io``
- Format: Add support for InfluxDB line protocol input format
- Source: Unlock reading from public S3 buckets anonymously (``--no-sign-request``)
- Source: Unlock and document reading from public Google Cloud Storage (GCS) buckets,
  and files on GitHub.
- Tests: Add "roadrunner" tests, using a bunch of external resources. The tests
  will only check for successful invocation, and not verify the generated SQL.
- Format: Add NetCDF input format
- AutoPK: Fix heuristics where the first column is a dictionary
- Format: Add GRIB2 input format
- Refactoring: Rework ``skeem.type``
- Refactoring: Add ``skeem.io.open`` as a wrapper around ``fsspec.open``
- Refactoring: Add ``skeem.io.to_dataframe`` from ``skeem.autopk``
- Refactoring: Add ``skeem.util`` folder instead of single ``util.py``
- UX: Add ``skeem info`` subcommand
- UX: Improve CLI help
- Format: Add support for reading compressed files in Gzip format
- CI: Run software tests on GHA
- CI: Use ``versioningit`` for automatic package versioning
- CI: Add OCI image builder to provide images for Podman, Docker, etc.
