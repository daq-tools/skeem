import logging
import sys
import typing as t
from pathlib import Path

import click

from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlTarget
from eskema.util import boot_click

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(package_name="eskema")
@click.option("--verbose", is_flag=True, required=False)
@click.option("--debug", is_flag=True, required=False)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, debug: bool):
    return boot_click(ctx, verbose, debug)


@cli.command("infer-ddl")
@click.argument("input", type=str, required=True)
@click.option("--content-type", type=str, required=False)
@click.option("--dialect", type=str, required=False)
@click.option("--table-name", type=str, required=False)
@click.option("--primary-key", type=str, required=False)
@click.pass_context
def infer_ddl(
    ctx: click.Context,
    input: t.Optional[t.Union[Path, str]] = None,  # noqa: A002
    content_type: t.Optional[str] = None,
    dialect: t.Optional[str] = None,
    table_name: t.Optional[str] = None,
    primary_key: t.Optional[str] = None,
):
    """
    Infer SQL DDL from input data.
    """
    indata: t.Union[t.IO, Path, str, None] = input
    path: t.Optional[Path] = None

    # Read data from stdin.
    if indata == "-":
        logger.info("Loading data from stdin")
        if not sys.stdin.readable():
            logger.error("stdin is not readable")
            sys.exit(-1)
        indata = sys.stdin

    # Read data from file.
    elif isinstance(indata, (Path, str)):
        path = Path(indata)
        logger.info(f"Loading data from '{path}'")
        indata = path.open("r")

    else:
        raise click.BadArgumentUsage("Unable to read data. 'input' argument missing or empty")

    # Decode data.
    sg = SchemaGenerator(
        resource=Resource(
            data=indata,
            path=path,
            content_type=content_type,
        ),
        target=SqlTarget(
            dialect=dialect,
            table_name=table_name,
            primary_key=primary_key,
        ),
    )
    result = sg.to_sql_ddl()
    print(result.pretty)  # noqa: T201

    indata.close()
