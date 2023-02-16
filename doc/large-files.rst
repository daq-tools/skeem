########################
Working with large files
########################


************
Introduction
************

Eskema tries to be efficient by only sampling the first few thousand records of
the obtained data source. The default values are currently:

- ``eskema.autopk.PEEK_LINES = 1000``
- ``eskema.sources.PEEK_LINES = 1000``
- ``eskema.model.PEEK_BYTES = 10000``
- ``frictionless.Detector.sample_size = 1000``


********
Examples
********

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

JSON::

    wget "https://data.cityofnewyork.us/resource/biws-g3hs.json"


.. _2017 Yellow Taxi Trip Data: https://data.cityofnewyork.us/Transportation/2017-Yellow-Taxi-Trip-Data/biws-g3hs
.. _New York City Taxi and Limousine Commission (TLC) Trip Record Data: https://registry.opendata.aws/nyc-tlc-trip-records-pds/
.. _NYC OpenData: https://opendata.cityofnewyork.us/
.. _Open Data on AWS: https://registry.opendata.aws/
