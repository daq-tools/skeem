import io
import json
import logging
import sys
import typing as t
from pathlib import Path

import click
from sqlformatter.sqlformatter import SQLFormatter


def jd(data):
    print(json.dumps(data, indent=2))  # noqa: T201


def sql_canonicalize(sql: str) -> str:
    return sql_pretty(sql)


def sql_pretty(sql: str, reindent: bool = False) -> str:
    sql = sql.strip().replace("\t", "    ")
    return SQLFormatter(
        reindent=reindent, indent_width=2, keyword_case="upper", identifier_case=None, comma_first=False
    ).format_query(sql)


def setup_logging(level=logging.INFO):

    # Define log format.
    log_format = "%(asctime)-15s [%(name)-26s] %(levelname)-7s: %(message)s"

    # Because `ddlgenerator` already invokes `logging.basicConfig()`, we need to apply `force`.
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level, force=True)

    # Disable `ddlgenerator` logger.
    root_logger = logging.getLogger("root")
    root_logger.disabled = True


def boot_click(ctx: click.Context, verbose: bool, debug: bool):

    # Adjust log level according to `verbose` / `debug` flags.
    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Setup logging, according to `verbose` / `debug` flags.
    setup_logging(level=log_level)


def get_firstline(data: t.Union[io.TextIOBase, Path, str]):
    if isinstance(data, io.TextIOBase):
        return stream_get_firstline(data)
    elif isinstance(data, str):
        return io.StringIO(data.splitlines()[0])
    elif isinstance(data, Path):
        data = Path(data)
        with open(data, "r") as f:
            return stream_get_firstline(f)
    else:
        raise TypeError(f"Unable to decode first line from data. type={type(data).__name__}")


def stream_get_firstline(stream: t.Union[io.TextIOBase, t.IO]):
    firstline = stream.readline()
    return io.StringIO(firstline.strip())
