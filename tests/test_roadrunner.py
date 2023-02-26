import pytest

from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlTarget

TIMEOUT_FAST = 1.5
TIMEOUT_MEDIUM = 3.5
TIMEOUT_SLOW = 7.5
TIMEOUT_ABYSMAL = 10

URL_LIST_FAST = [
    "github://daq-tools:eskema@/tests/testdata/basic.ods",
    "github://daq-tools:eskema@/tests/testdata/basic.xlsx",
    "github://daq-tools:eskema@/tests/testdata/basic-document.json",
    "https://github.com/daq-tools/eskema/raw/main/tests/testdata/basic.csv",
    "https://github.com/daq-tools/eskema/raw/main/tests/testdata/basic.lp",
    "https://github.com/influxdata/influxdb2-sample-data/raw/master/air-sensor-data/air-sensor-data.lp",
]

URL_LIST_MEDIUM = [
    "https://data.cityofnewyork.us/resource/biws-g3hs.csv",
    "https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_TEMP_TGL_2m_latlon0p5x0p5_2023022512_P003_all-products.grib2",
    "https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view",
    "https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view#gid=883324548",
    "https://www.unidata.ucar.edu/software/netcdf/examples/WMI_Lear.nc",
]

URL_LIST_SLOW = [
    "github://daq-tools:eskema@/tests/testdata/basic.csv",
    "https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_TEMP_TGL_2m_latlon0p5x0p5_2023022512_P003_all-products.grib2",
    "https://dd.weather.gc.ca/ensemble/geps/grib2/products/12/003/CMC_geps-prob_WIND_TGL_10m_latlon0p5x0p5_2023022512_P003_all-products.grib2",
    "https://dd.weather.gc.ca/analysis/precip/hrdpa/grib2/polar_stereographic/06/CMC_HRDPA_APCP-006-0100cutoff_SFC_0_ps2.5km_2023012606_000.grib2",
    "https://www.unidata.ucar.edu/software/netcdf/examples/sresa1b_ncar_ccsm3-example.nc",
]

URL_LIST_ABYSMAL = [
    "gs://tinybird-assets/datasets/guides/how-to-ingest-ndjson-data/events_100k.ndjson",
    "gs://tinybird-assets/datasets/nations.csv",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet",
    "https://data.cityofnewyork.us/resource/biws-g3hs.json",
    "s3://openaq-fetches/realtime/2023-02-25/1677351953_eea_2aa299a7-b688-4200-864a-8df7bac3af5b.ndjson",
    "s3://noaa-ghcn-pds/csv/by_year/2022.csv",
]


def urls(kind: str):
    if kind == "fast":
        val = URL_LIST_FAST
    elif kind == "medium":
        val = URL_LIST_MEDIUM
    elif kind == "slow":
        val = URL_LIST_SLOW
    elif kind == "abysmal":
        val = URL_LIST_ABYSMAL
    else:
        raise KeyError(f"Unknown url group for kind={kind}")
    for url in val:
        yield url


def to_sql(url: str):
    resource = Resource(path=url)
    sg = SchemaGenerator(
        resource=resource,
        target=SqlTarget(
            dialect="postgresql",
        ),
    )
    return sg.to_sql_ddl().canonical


@pytest.mark.roadrunner
@pytest.mark.timeout(TIMEOUT_FAST)
@pytest.mark.parametrize("url", urls("fast"))
def test_roadrunner_fast(url):
    sql = to_sql(url)
    assert "CREATE TABLE" in sql


@pytest.mark.roadrunner
@pytest.mark.timeout(TIMEOUT_MEDIUM)
@pytest.mark.parametrize("url", urls("medium"))
def test_roadrunner_medium(url):
    sql = to_sql(url)
    assert "CREATE TABLE" in sql


# @pytest.mark.xfail(run=False, reason="Too slow")
@pytest.mark.roadrunner
@pytest.mark.timeout(TIMEOUT_SLOW)
@pytest.mark.parametrize("url", urls("slow"))
def test_roadrunner_slow(url):
    sql = to_sql(url)
    assert "CREATE TABLE" in sql


@pytest.mark.roadrunner
@pytest.mark.timeout(TIMEOUT_ABYSMAL)
@pytest.mark.parametrize("url", urls("abysmal"))
def test_roadrunner_abysmal(url):
    sql = to_sql(url)
    assert "CREATE TABLE" in sql
