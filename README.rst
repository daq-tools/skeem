#####
Skeem
#####

|

.. start-badges

|ci-tests| |ci-coverage| |license| |pypi-downloads|
|python-versions| |status| |pypi-version|

.. |ci-tests| image:: https://github.com/daq-tools/skeem/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/daq-tools/skeem/actions/workflows/tests.yml

.. |ci-coverage| image:: https://codecov.io/gh/daq-tools/skeem/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/daq-tools/skeem
    :alt: Test suite code coverage

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/skeem.svg
    :target: https://pypi.org/project/skeem/

.. |status| image:: https://img.shields.io/pypi/status/skeem.svg
    :target: https://pypi.org/project/skeem/

.. |pypi-version| image:: https://img.shields.io/pypi/v/skeem.svg
    :target: https://pypi.org/project/skeem/

.. |pypi-downloads| image:: https://static.pepy.tech/badge/skeem/month
    :target: https://pypi.org/project/skeem/

.. |license| image:: https://img.shields.io/pypi/l/skeem.svg
    :target: https://github.com/daq-tools/skeem/blob/main/LICENSE

.. end-badges


*****
About
*****

Skeem infers SQL DDL statements from tabular data.

Skeem is, amongst others, based on the excellent `ddlgenerator`_,
`frictionless`_, `fsspec`_, `pandas`_, `ScipPy`_, `SQLAlchemy`_
and `xarray`_ packages, and can be used both as a standalone program,
and as a library.

Supported input data:

- `Apache Parquet`_
- `CSV`_
- `Google Sheets`_
- `GRIB`_
- `InfluxDB line protocol`_
- `JSON`_
- `NetCDF`_
- `NDJSON`_ (formerly LDJSON) aka. `JSON Lines`_, see also `JSON streaming`_
- `Office Open XML Workbook`_ (`Microsoft Excel`_)
- `OpenDocument Spreadsheet`_ (`LibreOffice`_)

Supported input sources:

- `Amazon S3`_
- `File system`_
- `GitHub`_
- `Google Cloud Storage`_
- `HTTP`_

Please note that Skeem is beta-quality software, and a work in progress.
Contributions of all kinds are very welcome, in order to make it more solid.
Breaking changes should be expected until a 1.0 release, so version pinning
is recommended, especially when you use it as a library.


********
Synopsis
********

.. code-block:: sh

    skeem infer-ddl --dialect=postgresql data.ndjson

.. code-block:: sql

    CREATE TABLE "data" (
        "id" SERIAL NOT NULL,
        "name" TEXT NOT NULL,
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "fruits" TEXT NOT NULL,
        "price" DECIMAL(2, 2) NOT NULL,
        PRIMARY KEY ("id")
    );


**********
Quickstart
**********

If you are in a hurry, and want to run Skeem without any installation, just use
the OCI image on Podman or Docker.

.. code-block:: sh

    docker run --rm ghcr.io/daq-tools/skeem-standard \
        skeem infer-ddl --dialect=postgresql \
        https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.ndjson


*****
Setup
*****

Install Skeem from PyPI.

.. code-block:: sh

    pip install skeem

Install Skeem with support for additional data formats like NetCDF.

.. code-block:: sh

    pip install 'skeem[scientific]'


*****
Usage
*****

This section outlines some example invocations of Skeem, both on the command
line, and per library use. Other than the resources available from the web,
testing data can be acquired from the repository's `testdata`_ folder.

Command line use
================

Help
----

.. code-block:: sh

    skeem info
    skeem --help
    skeem infer-ddl --help

Read from files
---------------

.. code-block:: sh

    # NDJSON, Parquet, and InfluxDB line protocol (ILP) formats.
    skeem infer-ddl --dialect=postgresql data.ndjson
    skeem infer-ddl --dialect=postgresql data.parquet
    skeem infer-ddl --dialect=postgresql data.lp

    # CSV, JSON, ODS, and XLSX formats.
    skeem infer-ddl --dialect=postgresql data.csv
    skeem infer-ddl --dialect=postgresql data.json
    skeem infer-ddl --dialect=postgresql data.ods
    skeem infer-ddl --dialect=postgresql data.xlsx
    skeem infer-ddl --dialect=postgresql data.xlsx --address="Sheet2"

Read from URLs
--------------

.. code-block:: sh

    # CSV, NDJSON, XLSX
    skeem infer-ddl --dialect=postgresql https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.csv
    skeem infer-ddl --dialect=postgresql https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.ndjson
    skeem infer-ddl --dialect=postgresql https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.xlsx --address="Sheet2"

    # Google Sheets: Address first sheet, and specific sheet of workbook.
    skeem infer-ddl --dialect=postgresql --table-name=foo https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view
    skeem infer-ddl --dialect=postgresql --table-name=foo https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view#gid=883324548

    # InfluxDB line protocol (ILP)
    skeem infer-ddl --dialect=postgresql https://github.com/influxdata/influxdb2-sample-data/raw/master/air-sensor-data/air-sensor-data.lp

    # Compressed files in gzip format
    skeem --verbose infer-ddl --dialect=crate --content-type=ndjson https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz

    # CSV on S3
    skeem --verbose infer-ddl --dialect=postgresql s3://noaa-ghcn-pds/csv/by_year/2022.csv

    # CSV on Google Cloud Storage
    skeem --verbose infer-ddl --dialect=postgresql gs://tinybird-assets/datasets/nations.csv
    skeem --verbose infer-ddl --dialect=postgresql gs://tinybird-assets/datasets/medals1.csv

    # CSV on GitHub
    skeem --verbose infer-ddl --dialect=postgresql github://daq-tools:skeem@/tests/testdata/basic.csv

    # GRIB2, NetCDF
    skeem infer-ddl --dialect=postgresql https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon/grib/18/t/icon-global_regular-lat-lon_air-temperature_level-90.grib2
    skeem infer-ddl --dialect=postgresql https://www.unidata.ucar.edu/software/netcdf/examples/sresa1b_ncar_ccsm3-example.nc
    skeem infer-ddl --dialect=postgresql https://www.unidata.ucar.edu/software/netcdf/examples/WMI_Lear.nc

OCI
---

OCI images are available on the GitHub Container Registry (GHCR). In order to
run them on Podman or Docker, invoke:

.. code-block:: sh

    docker run --rm ghcr.io/daq-tools/skeem-standard \
        skeem infer-ddl --dialect=postgresql \
        https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.csv

If you want to work with files on your filesystem, you will need to either
mount the working directory into the container using the ``--volume`` option,
or use the ``--interactive`` option to consume STDIN, like:

.. code-block:: sh

    docker run --rm --volume=$(pwd):/data ghcr.io/daq-tools/skeem-standard \
        skeem infer-ddl --dialect=postgresql /data/basic.ndjson

    docker run --rm --interactive ghcr.io/daq-tools/skeem-standard \
        skeem infer-ddl --dialect=postgresql --content-type=ndjson - < basic.ndjson

In order to always run the latest ``nightly`` development version, and to use a
shortcut for that, this section outlines how to use an alias for ``skeem``, and
a variable for storing the input URL. It may be useful to save a few keystrokes
on subsequent invocations.

.. code-block:: sh

    docker pull ghcr.io/daq-tools/skeem-standard:nightly
    alias skeem="docker run --rm --interactive ghcr.io/daq-tools/skeem-standard:nightly skeem"
    URL=https://github.com/daq-tools/skeem/raw/main/tests/testdata/basic.ndjson

    skeem infer-ddl --dialect=postgresql $URL


More
----

Use a different backend (default: ``ddlgen``)::

    skeem infer-ddl --dialect=postgresql --backend=frictionless data.ndjson

Reading data from STDIN needs to obtain both the table name and content type separately::

    skeem infer-ddl --dialect=crate --table-name=foo --content-type=ndjson - < data.ndjson

Reading data from STDIN also works like this, if you prefer to use pipes::

    cat data.ndjson | skeem infer-ddl --dialect=crate --table-name=foo --content-type=ndjson -


Library use
===========

.. code-block:: python

    import io
    from skeem.core import SchemaGenerator
    from skeem.model import Resource, SqlTarget

    INDATA = io.StringIO(
        """
        {"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
        {"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
        """
    )

    sg = SchemaGenerator(
        resource=Resource(data=INDATA, content_type="ndjson"),
        target=SqlTarget(dialect="crate", table_name="testdrive"),
    )

    print(sg.to_sql_ddl().pretty)

.. code-block:: sql

    CREATE TABLE "testdrive" (
        "id" INT NOT NULL,
        "name" STRING NOT NULL,
        "date" TIMESTAMP,
        "fruits" STRING NOT NULL,
        "price" DOUBLE NOT NULL,
        PRIMARY KEY ("id")
    );


***********
Development
***********

For installing the project from source, please follow the `development`_
documentation.


*******************
Project information
*******************

Credits
=======
- `Catherine Devlin`_ for `ddlgenerator`_ and `data_dispenser`_.
- `Mike Bayer`_ for `SQLAlchemy`_.
- `Paul Walsh`_ and `Evgeny Karev`_ for `frictionless`_.
- `Wes McKinney`_ for `pandas`_.
- All other countless contributors and authors of excellent Python
  packages, Python itself, and turtles all the way down.

Prior art
=========
We are maintaining a `list of other projects`_ with the same or similar goals
like Skeem.

Etymology
=========
The program was about to be called *Eskema*, but it turned out that there is
already another `Eskema`_ out there. So, it has been renamed to *Skeem*, which
is Estonian, and means "schema", "outline", or "(to) plan".



.. _Amazon S3: https://en.wikipedia.org/wiki/Amazon_S3
.. _Apache Parquet: https://en.wikipedia.org/wiki/Apache_Parquet
.. _Catherine Devlin: https://github.com/catherinedevlin
.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values
.. _data_dispenser: https://pypi.org/project/data_dispenser/
.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _development: doc/development.rst
.. _Eskema: https://github.com/nombrekeff/eskema
.. _Evgeny Karev: https://github.com/roll
.. _file system: https://en.wikipedia.org/wiki/File_system
.. _frictionless: https://github.com/frictionlessdata/framework
.. _fsspec: https://pypi.org/project/fsspec/
.. _GitHub: https://github.com/
.. _Google Cloud Storage: https://en.wikipedia.org/wiki/Google_Cloud_Storage
.. _Google Sheets: https://en.wikipedia.org/wiki/Google_Sheets
.. _GRIB: https://en.wikipedia.org/wiki/GRIB
.. _HTTP: https://en.wikipedia.org/wiki/HTTP
.. _InfluxDB line protocol: https://docs.influxdata.com/influxdb/latest/reference/syntax/line-protocol/
.. _JSON: https://www.json.org/
.. _JSON Lines: https://jsonlines.org/
.. _JSON streaming: https://en.wikipedia.org/wiki/JSON_streaming
.. _LibreOffice: https://en.wikipedia.org/wiki/LibreOffice
.. _list of other projects: doc/prior-art.rst
.. _Microsoft Excel: https://en.wikipedia.org/wiki/Microsoft_Excel
.. _Mike Bayer: https://github.com/zzzeek
.. _NDJSON: http://ndjson.org/
.. _NetCDF: https://en.wikipedia.org/wiki/NetCDF
.. _Office Open XML Workbook: https://en.wikipedia.org/wiki/Office_Open_XML
.. _OpenDocument Spreadsheet: https://en.wikipedia.org/wiki/OpenDocument
.. _pandas: https://pandas.pydata.org/
.. _Paul Walsh: https://github.com/pwalsh
.. _ScipPy: https://scipy.org/
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
.. _testdata: https://github.com/daq-tools/skeem/tree/main/tests/testdata
.. _Wes McKinney: https://github.com/wesm
.. _xarray: https://xarray.dev/
