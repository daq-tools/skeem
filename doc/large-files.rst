########################
Working with large files
########################


************
Introduction
************

It is always advised to acquire data files from remote locations to your
workstation. It will be so much easier and faster to work with, and will not
waste resources on subsequent redundant downloads.

However, there are situations where data files need to be accessed directly on
remote locations.

Eskema supports a variety of remote sources and data formats using the
excellent `fsspec`_ package, and tries to be efficient by only sampling the
first one hundred records of the obtained data source. The corresponding
default settings are currently:

- ``eskema.settings.PEEK_LINES = 100``
- ``eskema.settings.PEEK_BYTES = 13000``
- ``frictionless.Detector.sample_size = 100``


********
Examples
********


Finnish Meteorological Institute » Daily observations
=====================================================

Daily observations in 1km*1km grid » Interpolation.

Daily weather station observations have been interpolated into 1km*1km grid using
external predictors (e.g., elevation) as covariates (kriging with external drift KED).

Daily data is in annual netcdf files. The files are produced by R:s Raster package.

::

    aws s3 cp --no-sign-request s3://fmi-gridded-obs-daily-1km/Netcdf/Tday/tday_2023.nc .
    eskema --verbose infer-ddl --dialect=postgresql tday_2023.nc


OpenAQ
======

`OpenAQ`_ collects minutely global air quality data fetched from public data
sources all over the world, and harmonizes it into a free open-source data
platform.

This NDJSON file (115 MB) is from the `openaq-fetches`_ bucket on AWS S3::

    eskema --verbose infer-ddl --dialect=postgresql \
        s3://openaq-fetches/realtime/2023-02-25/1677351953_eea_2aa299a7-b688-4200-864a-8df7bac3af5b.ndjson


NOAA GHCN
=========

The `Global Historical Climatology Network (GHCN)`_, worth 200 years of global
climate data, is a data set of temperature, precipitation and pressure records
managed by the National Climatic Data Center (NDCC), Arizona State University
and the Carbon Dioxide Information Analysis Center.

This CSV file (1.2 GB) is from the `noaa-ghcn-pds`_ bucket on AWS S3::

    eskema --verbose infer-ddl --dialect=postgresql \
        s3://noaa-ghcn-pds/csv/by_year/2022.csv


NYC TLC
=======

The *New York City Taxi Trip Data* dataset published by the *New York City Taxi
and Limousine Commission (NYC TLC)* describes trips taken by taxis and for-hire
vehicles in New York City.

- The data in Parquet format is acquired from `New York City Taxi and Limousine
  Commission (TLC) Trip Record Data`_ at `Open Data on AWS`_.
- The data in NDJSON format is acquired from the ``crate.sampledata``
  sample data bucket on AWS S3.
- The data in CSV and JSON formats is acquired from `2017 Yellow Taxi Trip
  Data`_ at `NYC OpenData`_.

Parquet::

    wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
    eskema --verbose infer-ddl --dialect=postgresql yellow_tripdata_2022-01.parquet

    eskema --verbose infer-ddl --dialect=postgresql \
        https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet

NDJSON::

    wget https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz
    cat yc.2019.07.gz | gunzip > yc.2019.07.ndjson
    eskema --verbose infer-ddl --dialect=postgresql yc.2019.07.ndjson

CSV::

    # Acquire first 1000 lines of TLC trip data in CSV format, without needing to download everything.
    curl -s "https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD" \
        | dd bs=1 count=100000 | head -n 1000 > tlc-yc-2017-head.csv
    eskema --verbose infer-ddl --dialect=postgresql tlc-yc-2017-head.csv

    wget https://data.cityofnewyork.us/resource/biws-g3hs.csv
    eskema --verbose infer-ddl --dialect=postgresql biws-g3hs.csv

    # Try out both backends.
    eskema --verbose infer-ddl --dialect=postgresql --backend=ddlgen \
        https://data.cityofnewyork.us/resource/biws-g3hs.csv

    eskema --verbose infer-ddl --dialect=postgresql --backend=frictionless \
        https://data.cityofnewyork.us/resource/biws-g3hs.csv

JSON::

    wget https://data.cityofnewyork.us/resource/biws-g3hs.json
    eskema --verbose infer-ddl --dialect=postgresql biws-g3hs.json

    eskema --verbose infer-ddl --dialect=postgresql \
        https://data.cityofnewyork.us/resource/biws-g3hs.json


Ecommerce events
================

The `Tinybird » Ecommerce 100k rows NDJSON dataset`_ is used in their
`Tinybird » How to ingest NDJSON data`_ guide, it contains events from an
ecommerce website with different properties.

Reading NDJSON from remote resources is supported by both backends,
``ddlgen``, and ``frictionless``::

    eskema --verbose infer-ddl --dialect=postgresql --backend=ddlgen \
        https://storage.googleapis.com/tinybird-assets/datasets/guides/how-to-ingest-ndjson-data/events_100k.ndjson

    eskema --verbose infer-ddl --dialect=postgresql --backend=frictionless \
        https://storage.googleapis.com/tinybird-assets/datasets/guides/how-to-ingest-ndjson-data/events_100k.ndjson

You can also address public buckets in Google Cloud Storage, using the
``gs://`` scheme, like::

    eskema --verbose infer-ddl --dialect=postgresql \
        gs://tinybird-assets/datasets/guides/how-to-ingest-ndjson-data/events_100k.ndjson

.. _2017 Yellow Taxi Trip Data: https://data.cityofnewyork.us/Transportation/2017-Yellow-Taxi-Trip-Data/biws-g3hs
.. _fsspec: https://filesystem-spec.readthedocs.io/
.. _Global Historical Climatology Network (GHCN): https://en.wikipedia.org/wiki/Global_Historical_Climatology_Network
.. _Google Cloud Storage public datasets: https://cloud.google.com/storage/docs/public-datasets
.. _New York City Taxi and Limousine Commission (TLC) Trip Record Data: https://registry.opendata.aws/nyc-tlc-trip-records-pds/
.. _noaa-ghcn-pds: https://github.com/awslabs/open-data-registry/blob/main/datasets/noaa-ghcn.yaml#L4
.. _NYC OpenData: https://opendata.cityofnewyork.us/
.. _Open Data on AWS: https://registry.opendata.aws/
.. _OpenAQ: https://openaq.org/
.. _openaq-fetches: https://github.com/awslabs/open-data-registry/blob/main/datasets/openaq.yaml
.. _Tinybird » Ecommerce 100k rows NDJSON dataset: https://storage.googleapis.com/tinybird-assets/datasets/guides/how-to-ingest-ndjson-data/events_100k.ndjson
.. _Tinybird » How to ingest NDJSON data: https://www.tinybird.co/docs/guides/ingest-ndjson-data.html
