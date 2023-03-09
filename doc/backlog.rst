#############
Skeem backlog
#############


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
- [x] Format: Handle CSV
- [x] Format: Handle basic JSON: records + single document
- [x] Format: Handle spreadsheet formats: XLSX and ODF
- [x] Add more type annotations, and `mypy`_
- [x] Backend: Add `frictionless`_ backend
- [x] Tests: Add software tests for `frictionless`_ backend
- [x] Format: Add support for Google Sheets input format
- [x] Format: Add support for Parquet input format
- [x] Performance: Support reading large files efficiently
- [x] Source: Support reading data from HTTP
- [x] Performance: Support reading large files from HTTP more efficiently
- [x] Refactoring: A bit of code to ``skeem.io``
- [x] Format: Add support for "InfluxDB line protocol" input format
- [x] Refactoring: ``skeem.sources`` to ``skeem.ddlgen``?
- [x] Source: Support reading data from S3
- [x] Source: Load data from Google Cloud Storage
- [x] Format: Add NetCDF (.nc, .netcdf) input format
- [x] Format: Add GRIB2 (.grib2) input format
- [x] UX: ``skeem info``
- [x] UX: Add help texts to CLI options
- [x] Support reading archive files directly.

  - Example: https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz
  - https://github.com/leenr/gzip-stream

Bugs
====
- [x] Why is "frictionless" resource being read twice?

Documentation
=============
- [x] Inline code comments
- [x] Add "other projects" section
- [x] Document library use
- [x] Add example program
- [/] File headers
- [x] Replace https://raw.githubusercontent.com/ with https://github.com/foo/bar/raw/....

Infrastructure
==============
- [o] Add "examples" to test suite
- [o] CI/GHA
- [o] Docker build & publish
- [o] Docs: RTD
- [o] Release 0.1.0
- [o] Issue: Hello world

Quality
=======
- [x] QA: Use reference input test data from other repositories
- [x] QA: Use real-world data
- [x] Add "roadrunner" tests

Formats
=======
- [x] Format: Modernize ``skeem.type``
- [x] Format: Also recognize .netcdf, see https://en.ilmatieteenlaitos.fi/silam-opendata-on-aws-s3



***********
Iteration 3
***********


Formats
=======
- [o] Format: Add Zarr (.zarr) input format
- [o] Format: Add JSON5, YAML, TOML input formats
- [o] Format: Partitioned Geoparquet
  https://github.com/gadomski/chalkboard/blob/main/notebooks/isd-demo.ipynb
- [o] Format: dBase and friends
- [o] Format: Lance and ORC. -- https://github.com/eto-ai/lance
- [o] Format: CSV without headers: https://commonscreens.com/?page_id=1492


Bugs
====
- [o] Why is "ddlgen" resource being read twice? See ``_eval_lineprotocol``.
  => Workaround: Add ``@cachetools.func.lru_cache``
- [o] Can get hogged on resources like. Resolve: Automatically download before working on it.

  - https://www.unidata.ucar.edu/software/netcdf/examples/sresa1b_ncar_ccsm3-example.nc
  - s3://fmi-gridded-obs-daily-1km/Netcdf/Tday/tday_2022.nc
- [o] WMI_Lear.nc has "time" as "TIMESTAMP", but "sresa1b_ncar_ccsm3-example.nc" uses "TEXT"
- [o] Does not detect semicolon as field delimiter

  - https://archive.sensor.community/2015-10-01/2015-10-01_ppd42ns_sensor_27.csv
- [o] FrictionlessException: [source-error] The data source has not supported or has inconsistent contents: The HTTP server doesn't appear to support range requests. Only reading this file from the beginning is supported. Open with block_size=0 for a streaming file interface.

  - https://archive.sensor.community/parquet/2015-10/ppd42ns/part-00000-77c393f3-34ff-4e92-ad94-2c9839d70cd0-c000.snappy.parquet
- [o] RuntimeError: OrderedDict mutated during iteration

  - s3://openaq-fetches/realtime/2023-02-25/1677351953_eea_2aa299a7-b688-4200-864a-8df7bac3af5b.ndjson

- [o] Compute Engine Metadata server unavailable on attempt 1 of 3. Reason: timed out
- [o] Failed to decode variable 'valid_time': unable to decode time units 'seconds since 1970-01-01T00:00:00' with "calendar 'proleptic_gregorian'". Try opening your dataset with decode_times=False or installing cftime if it is not installed.

  - https://dd.weather.gc.ca/analysis/precip/hrdpa/grib2/polar_stereographic/06/CMC_HRDPA_APCP-006-0100cutoff_SFC_0_ps2.5km_2023012606_000.grib2
- [o] ``HTTP/1.1 403 Forbidden`` gets masked badly
- [o] Fix ``cat foo | --backend=fl -``
- [o] ``logger.warning`` will emit to STDOUT when running per tests

Features
========
- [o] Model/Type/Enum classes for backend and dataframe
- [o] Performance: Optimize loading from CSV
- [o] Source: Support reading data from HTTP, without file suffix, and/or query parameters
- [o] Source: Azure Blob Filesystem (ABFS), for accessing Planetary Computer
- [o] Library: Derive schema directly from pandas DataFrame, or others
- [o] IO: Export to descriptor and/or schema
- [o] Resource caching with fsspec? -- https://github.com/blaylockbk/Herbie/pull/153/files

Documentation
=============
- [o] Improve "library use" docs re. ``ContentType``

General
=======
- [o] Weird error: ``logger.warning("Unable to detect content type")`` will cause
  ``WARNING: Unable TO detect content TYPE`` to be written to STDOUT!?
- [o] Use ``smart_open``
  https://github.com/RaRe-Technologies/smart_open
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
- [o] Add decoder for C/C++ structs
  - https://getkotori.org/docs/gallery/lst.html
  - https://github.com/daq-tools/kotori/tree/main/kotori/vendor/lst
- [o] InfluxDB line protocol refinements

  - [o] Honor the ``measurement`` field, and map to table name
  - [o] Read irregular files, where field and tag names deviate between individual lines
  - [o] Use ``TIMESTAMP`` for ``time`` column?
- [o] Add support for other metrics formats. Prometheus, Graphite, collectd?
- [o] Enable ``frictionless`` backend using environment variable ``SKEEM_BACKEND=frictionless``
- [o] Provide options to control sample size
- [o] Startup time is currently one second. Can this be improved?
- [o] Add support for "InfluxDB annotated CSV" input format
- [o] Load Parquet files efficiently from S3
- [o] Unlock more fsspec sources

  - https://github.com/fsspec/filesystem_spec/blob/2023.1.0/setup.py#L41-L63
  - https://github.com/fsspec/filesystem_spec/blob/master/docs/source/api.rst#other-known-implementations
  - https://github.com/fsspec/dropboxdrivefs

- [o] Read data from Sensor.Community archive
- [o] Read data from IP to Country database
- [o] Format: Add HDF5 (.h5, .hdf) input format
- [o] Check ``fq``. -- https://github.com/wader/fq#supported-formats
- [o] GNU Poke

  - https://jemarch.net/poke
  - https://news.ycombinator.com/item?id=34986042
  - https://www.youtube.com/watch?v=KZ8meNZ_IhY
  - https://www.youtube.com/watch?v=XiR0Jq-nGr4
- [o] Check Hachoir

  - https://github.com/vstinner/hachoir
- quick and dirty script for generating avro ocf file with most data types
  https://gist.github.com/xentripetal/c0f1645ee1abd4d25f71896c8d650543
- [o] Use custom user agent

  - https://github.com/pandas-dev/pandas/issues/10526
  - https://github.com/pandas-dev/pandas/issues/36688
  - https://github.com/pandas-dev/pandas/pull/37966

Quality
=======
- [o] Is table- and field-name quoting properly applied for both backends?


***********
Iteration 4
***********

- [o] HTTP API endpoint
- [o] Add more input formats and sources

  - Parquet and friends
  - Fixed-width, using ``pd.read_fwf()``
  - Dataframes

    - Arrow / Datafusion
    - Dask
    - Ibis: https://github.com/ibis-project/ibis
    - Modin
    - Pandas
    - Polars
    - Spark
    - Vaex: https://github.com/vaexio/vaex
      https://vaex.io/blog/8-incredibly-powerful-Vaex-features-you-might-have-not-known-about
  - Avro
  - JSON Schema
  - XML, RDF, RSS

    - https://data.cityofnewyork.us/Transportation/2017-Yellow-Taxi-Trip-Data/biws-g3hs
    - https://catalog.data.gov/dataset/meteorite-landings
  - Spreadsheet formats: Microsoft pendant to Google Sheets, and friends
  - Tables from PDF and others
  - DuckDB can currently directly run queries on Parquet files, CSV files,
    SQLite files, Pandas, R and Julia data frames as well as Apache Arrow
    sources. This new extension adds the capability to directly query
    PostgreSQL tables from DuckDB.
    -- https://duckdb.org/2022/09/30/postgres-scanner.html
  - Read deeply nested JSON with DuckDB
    -- https://duckdb.org/2023/03/03/json.html

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
