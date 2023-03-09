#############################
Working with real-world files
#############################


************
Introduction
************

Evaluating Skeem with some files used the other day.


********
Examples
********


CMC GEPS NWP in GRIB2
=====================

`Global Ensemble Prediction System (GEPS)`_ `Numerical Weather Prediction (NWP)`_
data is published by the `Canadian Meteorological Centre (CMC)`_ in `GRIB2`_ format.

Synopsis::

    # Define URLs for `t2m` or `si10` data sets.
    URL=https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_TEMP_TGL_2m_latlon0p5x0p5_2023022512_P003_all-products.grib2
    URL=https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_WIND_TGL_10m_latlon0p5x0p5_2023022512_P003_all-products.grib2
    URL=https://dd.weather.gc.ca/analysis/precip/hrdpa/grib2/polar_stereographic/06/CMC_HRDPA_APCP-006-0100cutoff_SFC_0_ps2.5km_2023012606_000.grib2

    skeem --verbose infer-ddl --dialect=postgresql $URL


OpenAQ
======

`OpenAQ`_ collects minutely global air quality data fetched from public data
sources all over the world, and harmonizes it into a free open-source data
platform.

This NDJSON file (115 MB) is from the `openaq-fetches`_ bucket on AWS S3::

    skeem --verbose infer-ddl --dialect=postgresql \
        s3://openaq-fetches/realtime/2023-02-25/1677351953_eea_2aa299a7-b688-4200-864a-8df7bac3af5b.ndjson


Finnish Meteorological Institute » Daily observations
=====================================================

Daily observations in 1km*1km grid » Interpolation, see `FMI gridded observations on AWS S3`_.

Daily weather station observations have been interpolated into 1km*1km grid using
external predictors (e.g., elevation) as covariates (kriging with external drift KED).

Daily data is in annual netcdf files. The files are produced by R:s Raster package.

This NetCDF file (170 MB) is from the `fmi-gridded-obs-daily-1km`_ bucket on AWS S3::

    aws s3 cp --no-sign-request s3://fmi-gridded-obs-daily-1km/Netcdf/Tday/tday_2023.nc .
    skeem --verbose infer-ddl --dialect=postgresql tday_2023.nc


Sensor.Community
================

TODO
----
- https://archive.sensor.community/2015-10-01/2015-10-01_ppd42ns_sensor_27.csv
- https://archive.sensor.community/parquet/2015-10/ppd42ns/part-00000-77c393f3-34ff-4e92-ad94-2c9839d70cd0-c000.snappy.parquet


.. _Canadian Meteorological Centre (CMC): https://weather.gc.ca/
.. _FMI gridded observations on AWS S3: https://en.ilmatieteenlaitos.fi/gridded-observations-on-aws-s3
.. _FMI radar data on AWS S3: https://en.ilmatieteenlaitos.fi/radar-data-on-aws-s3
.. _Global Ensemble Prediction System (GEPS): https://weather.gc.ca/grib/grib2_ens_geps_e.html
.. _GRIB2: https://en.wikipedia.org/wiki/GRIB
.. _OpenAQ: https://openaq.org/
.. _openaq-fetches: https://github.com/awslabs/open-data-registry/blob/main/datasets/openaq.yaml
.. _Numerical Weather Prediction (NWP): https://en.wikipedia.org/wiki/Numerical_Weather_Prediction
