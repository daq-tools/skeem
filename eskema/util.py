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


def boot_click(ctx: click.Context, verbose: bool, debug: bool):

    # Adjust log level according to `verbose` / `debug` flags.
    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Setup logging, according to `verbose` / `debug` flags.
    setup_logging(level=log_level)


def get_firstline(data: t.Union[io.TextIOBase, Path, str], nrows: int = 1):
    if isinstance(data, io.TextIOBase):
        return stream_get_firstline(data, nrows=nrows)
    elif isinstance(data, str):
        return str_get_firstline(data, nrows=nrows)
    elif isinstance(data, Path):
        data = Path(data)
        with open(data, "r") as f:
            return stream_get_firstline(f, nrows=nrows)
    else:
        raise TypeError(f"Unable to decode first {nrows} line(s) from data. type={type(data).__name__}")


def stream_get_firstline(stream: t.Union[io.TextIOBase, t.IO], nrows: int = 1):
    buffer = io.StringIO()
    for _ in range(nrows):
        buffer.write(stream.readline())
    buffer.seek(0)
    return buffer


def str_get_firstline(data: str, nrows: int = 1):
    buffer = io.StringIO()
    lines = data.splitlines()[:nrows]
    for line in lines:
        buffer.write(line)
    buffer.seek(0)
    return buffer
