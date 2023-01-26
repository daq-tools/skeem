import logging
import sys
import typing as t
from pathlib import Path

import click

from eskema.core import generate_ddl
from eskema.util import boot_click, sql_canonicalize, sql_pretty

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(package_name="eskema")
@click.option("--verbose", is_flag=True, required=False)
@click.option("--debug", is_flag=True, required=False)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, debug: bool):
    return boot_click(ctx, verbose, debug)


@cli.command("infer-ddl")
@click.option("--dialect", type=str, required=True)
@click.option("--table-name", type=str, required=False)
@click.option("--primary-key", type=str, required=False)
@click.argument("input", type=str, required=True)
@click.pass_context
def infer_ddl(
    ctx: click.Context,
    dialect: str,
    table_name: t.Optional[str] = None,
    primary_key: t.Optional[str] = None,
    input: t.Optional[t.Union[Path, str]] = None,  # noqa: A002
):
    """
    Infer SQL DDL from input data.
    """
    indata = input
    path: t.Optional[Path] = None

    # Read data from stdin.
    # TODO: Can also leave empty?
    if indata == "-":
        logger.info("Loading data from stdin")
        if not sys.stdin.readable():
            logger.error("stdin is not readable")
            sys.exit(-1)
        indata = sys.stdin

    # Read data from file.
    else:
        path = Path(indata)
        indata = path.open("r")
        logger.info(f"Loading data from {indata}")

    # Derive table name from input file name or data.
    if table_name is None and path is not None:
        table_name = path.stem

    # Decode data.
    sql = generate_ddl(indata, table_name=table_name, primary_key=primary_key)
    sql = sql_canonicalize(sql)
    print(sql_pretty(sql))  # noqa: T201
    logger.info("Ready.")

    indata.close()
