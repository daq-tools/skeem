import logging
import pathlib
import sys
import typing as t

import click

from eskema.core import generate_ddl, get_firstline
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
@click.argument("input", type=str, required=True)
@click.pass_context
def infer_ddl(
    ctx: click.Context,
    dialect: str,
    table_name: t.Optional[str] = None,
    input: t.Optional[t.Union[pathlib.Path, str]] = None,  # noqa: A002
):
    """
    Infer SQL DDL from input data.
    """
    indata = input
    # TODO: Can also leave empty?
    if indata == "-":
        logger.info("Loading data from stdin")
        if not sys.stdin.readable():
            logger.error("stdin is not readable")
            sys.exit(-1)
        indata = sys.stdin
    else:
        indata = pathlib.Path(indata)
        logger.info(f"Loading data from {indata}")
    firstline = get_firstline(indata)
    # TODO: Derive table name from input file name.
    sql = generate_ddl(firstline, table_name=table_name, primary_key="id")
    sql = sql_canonicalize(sql)
    print(sql_pretty(sql))  # noqa: T201
    logger.info("Ready.")
