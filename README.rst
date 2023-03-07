.. highlight:: sh


######
Eskema
######


*****
About
*****

You can use Eskema to infer SQL DDL statements from tabular data.

Eskema is based on the excellent `ddlgenerator`_, `frictionless`_, `fsspec`_,
`pandas`_, `SQLAlchemy`_, `xarray`_ packages and friends, and can be used both
as a standalone program, and as a library.

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


********
Synopsis
********

.. code-block:: sh

    eskema info

.. code-block:: sh

    eskema infer-ddl --dialect=postgresql data.ndjson

.. code-block:: sql

    CREATE TABLE "data" (
        "id" SERIAL NOT NULL,
        "name" TEXT NOT NULL,
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "fruits" TEXT NOT NULL,
        "price" DECIMAL(2, 2) NOT NULL,
        PRIMARY KEY ("id")
    );


*****
Setup
*****

.. code-block:: sh

    pip install eskema

    # Additional formats: NetCDF
    pip install 'eskema[scientific]'


*****
Usage
*****

This section display some example invocations of Eskema, both on the command
line, and per library use. Other than the resources available from the web,
testing data can be acquired from the repository's `testdata`_ folder.

Command line use
================

Read data from given file::

    # NDJSON, Parquet, and InfluxDB line protocol (ILP) formats.
    eskema infer-ddl --dialect=postgresql data.ndjson
    eskema infer-ddl --dialect=postgresql data.parquet
    eskema infer-ddl --dialect=postgresql data.lp

    # CSV, JSON, ODS, and XLSX formats.
    eskema infer-ddl --dialect=postgresql data.csv
    eskema infer-ddl --dialect=postgresql data.json
    eskema infer-ddl --dialect=postgresql data.ods
    eskema infer-ddl --dialect=postgresql data.xlsx
    eskema infer-ddl --dialect=postgresql data.xlsx --address="Sheet2"

    # GRIB2, NetCDF
    eskema infer-ddl --dialect=postgresql https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_TEMP_TGL_2m_latlon0p5x0p5_2023022512_P003_all-products.grib2
    eskema infer-ddl --dialect=postgresql https://www.unidata.ucar.edu/software/netcdf/examples/sresa1b_ncar_ccsm3-example.nc
    eskema infer-ddl --dialect=postgresql https://www.unidata.ucar.edu/software/netcdf/examples/WMI_Lear.nc

Read data from URL::

    # CSV, NDJSON, XLSX
    eskema infer-ddl --dialect=postgresql https://github.com/daq-tools/eskema/raw/main/tests/testdata/basic.csv
    eskema infer-ddl --dialect=postgresql https://github.com/daq-tools/eskema/raw/main/tests/testdata/basic.ndjson
    eskema infer-ddl --dialect=postgresql https://github.com/daq-tools/eskema/raw/main/tests/testdata/basic.xlsx --address="Sheet2"

    # Google Sheets: Address first sheet, and specific sheet of workbook.
    eskema infer-ddl --dialect=postgresql --table-name=foo https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view
    eskema infer-ddl --dialect=postgresql --table-name=foo https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view#gid=883324548

    # InfluxDB line protocol (ILP)
    eskema infer-ddl --dialect=postgresql https://github.com/influxdata/influxdb2-sample-data/raw/master/air-sensor-data/air-sensor-data.lp

    # CSV on S3
    eskema --verbose infer-ddl --dialect=postgresql s3://noaa-ghcn-pds/csv/by_year/2022.csv

    # CSV on Google Cloud Storage
    eskema --verbose infer-ddl --dialect=postgresql gs://tinybird-assets/datasets/nations.csv
    eskema --verbose infer-ddl --dialect=postgresql gs://tinybird-assets/datasets/medals1.csv

    # CSV on GitHub
    eskema --verbose infer-ddl --dialect=postgresql github://daq-tools:eskema@/tests/testdata/basic.csv

Use a different backend (default: ``ddlgen``)::

    eskema infer-ddl --dialect=postgresql --backend=frictionless data.ndjson

Reading data from stdin needs to obtain both the table name and content type separately::

    eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson - < data.ndjson
    eskema infer-ddl --dialect=crate --table-name=foo --content-type=json - < data.json
    eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv - < data.csv

Reading data from stdin also works like this, if you prefer to use pipes::

    cat data.ndjson | eskema infer-ddl --dialect=crate --table-name=foo --content-type=ndjson -
    cat data.json | eskema infer-ddl --dialect=crate --table-name=foo --content-type=json -
    cat data.csv | eskema infer-ddl --dialect=crate --table-name=foo --content-type=csv -


Library use
===========

.. code-block:: python

    import io
    from eskema.core import SchemaGenerator
    from eskema.model import Resource, SqlTarget

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

For working with the latest development version, please follow the
`development`_ documentation.


*********************
Credits and prior art
*********************

- `Mike Bayer`_ for `SQLAlchemy`_.
- `Catherine Devlin`_ for `ddlgenerator`_ and `data_dispenser`_.
- `Paul Walsh`_ and `Evgeny Karev`_ for `frictionless`_.
- All the other countless authors of excellent Python packages,
  Python itself, and turtles all the way down.
- More prior art: We are maintaining a `list of other projects`_ with the same
  or similar goals like Eskema.


.. _Amazon S3: https://en.wikipedia.org/wiki/Amazon_S3
.. _Apache Parquet: https://en.wikipedia.org/wiki/Apache_Parquet
.. _Catherine Devlin: https://github.com/catherinedevlin
.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values
.. _data_dispenser: https://pypi.org/project/data_dispenser/
.. _ddlgenerator: https://pypi.org/project/ddlgenerator/
.. _development: doc/development.rst
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
.. _pandas: https://pypi.org/project/pandas/
.. _Paul Walsh: https://github.com/pwalsh
.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy/
.. _testdata: https://github.com/daq-tools/eskema/tree/main/tests/testdata
.. _xarray: https://xarray.dev/
