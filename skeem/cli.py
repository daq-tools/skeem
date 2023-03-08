import logging
import sys
import typing as t
from pathlib import Path

import click

from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlTarget
from skeem.report import AboutReport
from skeem.util.cli import boot_click, docstring_format_verbatim, split_list

logger = logging.getLogger(__name__)


def help_infer_ddl():
    """
    Infer SQL DDL from input data.

    INPUT can be a file or a URL.

    Synopsis
    --------

    Use data in NDJSON format:

      skeem infer-ddl --dialect=postgresql data.ndjson

    Generated SQL DDL:

      CREATE TABLE "data" (
        "id" SERIAL NOT NULL,
        "name" TEXT NOT NULL,
        "date" TIMESTAMP WITHOUT TIME ZONE,
        "fruits" TEXT NOT NULL,
        "price" DECIMAL(2, 2) NOT NULL,
        PRIMARY KEY ("id")
      );

    Examples
    --------

      # NDJSON, Parquet, and InfluxDB line protocol (ILP) formats
      skeem infer-ddl --dialect=postgresql data.ndjson
      skeem infer-ddl --dialect=postgresql data.parquet
      skeem infer-ddl --dialect=postgresql data.lp

      # CSV, JSON, ODS, and XLSX formats
      skeem infer-ddl --dialect=postgresql data.csv
      skeem infer-ddl --dialect=postgresql data.json
      skeem infer-ddl --dialect=postgresql data.ods
      skeem --verbose infer-ddl --dialect=postgresql data.xlsx
      skeem --verbose infer-ddl --dialect=postgresql data.xlsx --address="Sheet2"

      # Google Sheets
      skeem infer-ddl --dialect=postgresql --table-name=foo https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view

      # InfluxDB line protocol (ILP)
      skeem infer-ddl --dialect=postgresql https://github.com/influxdata/influxdb2-sample-data/raw/master/air-sensor-data/air-sensor-data.lp

      # Compressed files in gzip format
      skeem infer-ddl --content-type=ndjson --dialect=crate https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz

      ... and a lot more!

    Documentation
    -------------

    More options and examples can be discovered on the Skeem README [1].

    [1] https://github.com/daq-tools/skeem/blob/main/README.rst
    """  # noqa: E501


@click.group()
@click.version_option(package_name="skeem")
@click.option("--verbose", is_flag=True, required=False, help="Turn on logging")
@click.option("--debug", is_flag=True, required=False, help="Turn on logging with debug level")
@click.option(
    "--trace-modules",
    is_flag=False,
    show_default=True,
    required=False,
    type=click.STRING,
    help="Set modules to be traced (comma-separated list)",
    callback=lambda ctx, param, value: split_list(value),
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, debug: bool, trace_modules: t.List[str]):
    return boot_click(ctx, verbose, debug, trace_modules)


@cli.command("info", help="Report about available content types and platform information")
def info():
    AboutReport.types()
    AboutReport.platform()


@cli.command(
    "infer-ddl",
    help=docstring_format_verbatim(help_infer_ddl.__doc__),
    context_settings={"max_content_width": 120},
)
@click.argument("input", type=str, required=True)
@click.option("--dialect", type=str, required=False, help="Select SQLAlchemy dialect for generating SQL")
@click.option("--table-name", type=str, required=False, help="Specify table name used in DDL statement")
@click.option(
    "--primary-key",
    type=str,
    required=False,
    help="Specify primary key when it can not be inferred, or is inferred erroneously",
)
@click.option("--content-type", type=str, required=False, help="Specify content type when data is read from STDIN")
@click.option(
    "--address", type=str, required=False, help="Optionally address sub-resources like tabs within spreadsheets"
)
@click.option(
    "--backend",
    type=click.Choice(["ddlgen", "frictionless", "fl"]),
    required=False,
    default="ddlgen",
    help="Select backend for inferring data types. Default: ddlgen",
)
@click.pass_context
def infer_ddl(
    ctx: click.Context,
    input: t.Optional[t.Union[Path, str]] = None,  # noqa: A002
    address: t.Optional[str] = None,
    content_type: t.Optional[str] = None,
    dialect: t.Optional[str] = None,
    table_name: t.Optional[str] = None,
    primary_key: t.Optional[str] = None,
    backend: t.Optional[str] = "ddlgen",
):
    indata: t.Union[t.IO, Path, str, None] = input
    path: t.Optional[t.Union[Path, str]] = None

    # Read data from stdin.
    if indata == "-":
        logger.info("Loading data from stdin")
        if not sys.stdin.readable():
            logger.error("stdin is not readable")
            sys.exit(-1)
        indata = sys.stdin.buffer

    # Read data from file.
    elif isinstance(indata, (Path, str)):
        path = indata
        logger.info(f"Loading data from: {path}")
        indata = None

    # Decode data.
    sg = SchemaGenerator(
        resource=Resource(
            data=indata,
            address=address,
            path=path,
            content_type=content_type,
        ),
        target=SqlTarget(
            dialect=dialect,
            table_name=table_name,
            primary_key=primary_key,
        ),
        backend=backend,
    )

    # Convert to SQL DDL.
    result = sg.to_sql_ddl()
    print(result.pretty)  # noqa: T201

    if indata is not None:
        indata.close()
