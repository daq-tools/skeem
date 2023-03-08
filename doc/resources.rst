#########################
Skeem resource collection
#########################


Azure Blob Filesystem (ABFS)
============================
Also: Planetary Computer

- planetarycomputer://stac/v1/era5-pds/era5-pds-1980-01-fc?datetime=1980-01
- planetarycomputer://stac/v1/era5-pds/era5-pds-1980-01-an?datetime=1980-01
- https://planetarycomputer.microsoft.com/api/stac/v1/collections/era5-pds
- https://planetarycomputer.microsoft.com/api/stac/v1/collections/era5-pds/items/era5-pds-2020-12-fc
- abfs://era5/ERA5/2020/12/air_temperature_at_2_metres_1hour_Maximum.zarr
- abfs://era5/ERA5/2020/12/precipitation_amount_1hour_Accumulation.zarr
- pandas.read_csv('abfs[s]://
https://learn.microsoft.com/en-us/azure/synapse-analytics/spark/tutorial-use-pandas-spark-pool


Archive files
=============

- https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz
- IP to Country database

  - https://db-ip.com/db/format/ip-to-city-lite/csv.html
  - http://download.db-ip.com/free/dbip-city-lite-2023-02.csv.gz

- https://archive.sensor.community/csv_per_month/2015-10/2015-10_ppd42ns.zip
- https://opendata.dwd.de/weather/nwp/icon-d2/grib/00/t_2m/icon-d2_germany_icosahedral_single-level_2023022600_000_2d_t_2m.grib2.bz2


CSV
===

- https://catalog.data.gov/dataset/meteorite-landings
- https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD
- https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD
- s3://gdelt-open-data/events/20190918.export.csv (with backend=fl)
- s3://noaa-ghcn-pds/csv/by_year/2022.csv
- gs://tinybird-assets/datasets/nations.csv


Google Cloud Storage
====================

- https://github.com/google/youtube-8m
- gs://youtube8m-ml
- https://research.google.com/youtube8m/download.html


InfluxDB
========

Line protocol, annotated CSV, and extended annotated CSV.

- https://github.com/influxdata/influxdb2-sample-data
- https://github.com/influxdata/influxdb2-sample-data/blob/master/air-sensor-data/air-sensor-data-annotated.csv
- https://github.com/influxdata/influxdb2-sample-data/blob/master/air-sensor-data/air-sensor-data.lp

Small files:
- https://github.com/Anaisdg/GettingStarted_WritingPoints/blob/master/Data/chronograf.txt

Large files:
- https://github.com/Anaisdg/GettingStarted_WritingPoints/blob/master/Data/import.txt


NetCDF and HDF
==============

- https://en.ilmatieteenlaitos.fi/open-data-on-aws-s3
- https://en.ilmatieteenlaitos.fi/gridded-observations-on-aws-s3
- s3://fmi-gridded-obs-daily-1km/Netcdf/Tday/tday_2022.nc
- https://www.unidata.ucar.edu/software/netcdf/examples/files.html
- https://stackoverflow.com/questions/54629358/loading-hdf5-files-into-python-xarrays
- https://docs.h5py.org/en/stable/high/dataset.html
- https://extremeweatherdataset.github.io/
- http://s3-eu-west-1.amazonaws.com/fmi-opendata-radar-volume-hdf5/2007/01/01/fianj/200701010825_fianj_PVOL.h5



Online spreadsheets
===================

- Google Drive at ``drive.google.com`` or ``docs.google.com``:

  - | https://docs.google.com/file/d/1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz/view
    | ``http "https://drive.google.com/uc?export=download&id=1v7x-s79pQUV3ayVfTAeUG-xsXRHTQ9iz" --follow``

- Google Sheets:

  - VES:

    - basic: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/edit
    - Sheet2: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/edit#gid=883324548
  - CSV:

    - basic: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=csv
    - Sheet2: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?gid=883324548&format=csv
  - XLSX: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=xlsx
  - ODS: https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/export?format=ods
  - More formats: tsv, zip, pdf

- Google AppSheet App:

  - https://www.appsheet.com/Template/AppDef?appName=basic-285352295&appId=f6f7024c-5ab6-46c1-863b-c446eb2f4c28&channel=gdrive
  - Table editor: https://www.appsheet.com/Template/AppDef?appName=basic-285352295#Data.Tables.basic
  - Table view: https://www.appsheet.com/template/showtable?appId=basic-285352295&tableName=basic
  - Share » Editor: https://www.appsheet.com/Template/AppDef?appName=basic-285352295&utm_source=share_app_link
  - Share » Browser: https://www.appsheet.com/start/f6f7024c-5ab6-46c1-863b-c446eb2f4c28
  - Share » Install: https://www.appsheet.com/newshortcut/f6f7024c-5ab6-46c1-863b-c446eb2f4c28
  - Report » Looker Studio: https://lookerstudio.google.com/reporting/create?c.mode=edit&c.reportId=8225cc90-e702-42a1-9d9b-4aca626f6d1e&c.explain=true&ds.connector=COMMUNITY&ds.deploymentId=AKfycbxy0_bVIUsKVRWtvA0fJfEq_F_wdP2whFOQGskykubSizkpmQojrOFMe1EN9rz6klk0&ds.appId=f6f7024c-5ab6-46c1-863b-c446eb2f4c28&ds.tableName=basic&ds.refreshFields=true&plugin.id=AppSheet&plugin.report=%7B%20%22v1%22:%20%7B%20%22t%22:%20%22basic:%20basic%22,%20%22c%22:%20%7B%20%7D,%20%22b%22:%20%7B%20%22t%22:%20%7B%20%22d%22:%20%5B%20%22name%22,%20%22date%22,%20%22fruits%22%20%5D,%20%22m%22:%20%5B%20%7B%20%22d%22:%20%22price%22,%20%22a%22:%20%22METRIC_AGGREGATION_MAX%22%20%7D%20%5D%20%7D%20%7D%20%7D%20%7D

- AppSheet database, table »basic«:

  - Edit: https://www.appsheet.com/dbs/database/sqnDBz26zA4gU-gNcB8eZa/table/EmXXq1RtFn4a2elXmJ3Le4
  - Share: https://www.appsheet.com/dbs/database/sqnDBz26zA4gU-gNcB8eZa

- TODO: Google AppSheet » New table » New source » On-premises database » Add DreamFactory connection » Postgres

  - https://www.appsheet.com/Account/DreamFactoryAuthInfo?state=e2a33e28-9026-46d8-8230-93c36fbc837d
  - https://www.dreamfactory.com/


S3 resources
============

- https://auth0.com/blog/fantastic-public-s3-buckets-and-how-to-find-them/
- https://registry.opendata.aws/tag/parquet/
- https://github.com/aws-samples/data-lake-as-code
- Daylight Map Distribution of OpenStreetMap

  - https://github.com/awslabs/open-data-registry/blob/4b7daa433f661e9160caad0c997e2b98344bc6bf/datasets/daylight-osm.yaml#L4
  - 536MB: s3://daylight-openstreetmap/parquet/osm_features/release=v1.23/type=node/20230213_194556_00133_znrw2_0b5d6e91-1c32-48a9-b821-92d190d082a7

- Common Screens, OpenAQ, NOAA GHCN

  - 800MB: s3://common-screens/source-data/source-a.csv
  - 78MB: s3://openaq-fetches/daily/2017-09-07.csv
  - 114MB: s3://openaq-fetches/realtime/2023-02-25/1677351953_eea_2aa299a7-b688-4200-864a-8df7bac3af5b.ndjson
  - 52MB: s3://noaa-ghcn-pds/parquet/by_station/STATION=ASN00040600/ELEMENT=PRCP/7bfb17089ff64ed086708bd31c11b2a9_0.snappy.parquet
  - 1.3GB: s3://noaa-ghcn-pds/csv/by_year/2022.csv


Zarr
====

- https://cmip6-pds.s3.amazonaws.com/index.html#CMIP6/
- https://cloud.google.com/storage/docs/public-datasets/era5
- https://pangeo-data.github.io/pangeo-cmip6-cloud/overview.html
- https://en.ilmatieteenlaitos.fi/silam-opendata-on-aws-s3
