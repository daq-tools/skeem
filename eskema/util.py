import json
import logging
import sys

import click
from sqlformatter.sqlformatter import SQLFormatter


def jd(data):
    print(json.dumps(data, indent=2))  # noqa: T201


def sql_canonicalize(sql: str) -> str:
    return sql_pretty(sql)


def sql_pretty(sql: str) -> str:
    sql = sql.strip().replace("\t", "    ")
    return SQLFormatter(
        reindent=False, indent_width=2, keyword_case="upper", identifier_case=None, comma_first=False
    ).format_query(sql)


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-26s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)

    # Adjust log format for "root" logger, used by `ddlgenerator`.
    root_logger = logging.getLogger("root")
    root_logger.setLevel(level=level)
    root_logger.handlers[0].setFormatter(logging.Formatter(log_format))

    # Disable `ddlgenerator` logger.
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
