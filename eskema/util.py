import io
import json
import logging
import sys
import typing as t
from collections import OrderedDict
from pathlib import Path

import click
import json_stream
from json_stream.base import StreamingJSONList, StreamingJSONObject
from sqlformatter.sqlformatter import SQLFormatter

logger = logging.getLogger(__name__)


def jd(data: t.Any):
    """
    Pretty-print JSON with indentation.
    """
    print(json.dumps(data, indent=2))  # noqa: T201


def sql_canonicalize(sql: str) -> str:
    """
    Compute canonical representation for SQL statement.
    """
    return sql_pretty(sql)


def sql_pretty(sql: str, reindent: bool = False) -> str:
    """
    Prettify SQL statement.
    """
    sql = sql.strip().replace("\t", "    ")
    return SQLFormatter(
        reindent=reindent, indent_width=2, keyword_case="upper", identifier_case=None, comma_first=False
    ).format_query(sql)


def setup_logging(level=logging.INFO):
    """
    Setup loggers.
    """

    # Define log format.
    log_format = "%(asctime)-15s [%(name)-34s] %(levelname)-7s: %(message)s"

    # Because `ddlgenerator` already invokes `logging.basicConfig()`, we need to apply `force`.
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level, force=True)

    # Disable `ddlgenerator` logger.
    # root_logger = logging.getLogger("root")  # noqa: ERA001
    # root_logger.disabled = True  # noqa: ERA001


def boot_click(ctx: click.Context, verbose: bool = False, debug: bool = False, trace_modules: t.List[str] = None):
    """
    Bootstrap the CLI application.
    """
    trace_modules = trace_modules or []

    # Adjust log level according to `verbose` / `debug` flags.
    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Setup logging, according to `verbose` / `debug` flags.
    setup_logging(level=log_level)

    # Optionally enable code tracing.
    if trace_modules:
        enable_tracing(modules=trace_modules)


def get_firstline(data: t.Union[io.TextIOBase, Path, str], nrows: int = 1) -> t.IO:
    """
    Get first N lines of input data.
    """
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


def stream_get_firstline(stream: t.Union[io.TextIOBase, t.IO], nrows: int = 1) -> t.IO:
    """
    Get first N lines of input data from stream.
    """
    buffer = io.StringIO()
    for _ in range(nrows):
        buffer.write(stream.readline())
    buffer.seek(0)
    return buffer


def str_get_firstline(data: str, nrows: int = 1) -> t.IO:
    """
    Get first N lines of input data from str.
    """
    buffer = io.StringIO()
    lines = data.splitlines()[:nrows]
    for line in lines:
        buffer.write(line)
    buffer.seek(0)
    return buffer


def json_get_first_records(data: io.TextIOBase, nrecords: int = 5) -> t.List[t.OrderedDict[t.AnyStr, t.Any]]:
    """
    Read JSON data lazily, without loading the whole document into memory.

    - From a "list of objects" JSON document, get only the first N records.
    - From a "single object" JSON document, get only the first record.
    """
    try:
        stream = json_stream.load(data)
    except StopIteration as ex:
        raise ValueError("Unable to parse JSON document in streaming mode. Reason: Document is empty") from ex
    except Exception as ex:
        raise ValueError(f"Unable to parse JSON document in streaming mode. Reason: {ex}") from ex

    if isinstance(stream, StreamingJSONList):
        records = []
        for index in range(nrecords):
            try:
                record = OrderedDict(stream[index].items())
                records.append(record)
            except IndexError:
                break
        return records

    elif isinstance(stream, StreamingJSONObject):
        record = OrderedDict(stream.items())
        records = [record]
        return records

    return []  # pragma: no cover


def to_bytes(payload: t.Union[str, bytes], name: t.Optional[str] = None) -> io.BytesIO:
    if isinstance(payload, str):
        payload = payload.encode()
    data = io.BytesIO(payload)
    data.name = name or "UNKNOWN"
    return data


def split_list(value: str, delimiter: str = ",") -> t.List[str]:
    if value is None:
        return []
    return [c.strip() for c in value.split(delimiter)]


def to_list(x: t.Any, default: t.List[t.Any] = None) -> t.List[t.Any]:
    if not isinstance(default, t.List):
        raise ValueError("Default value is not a list")
    if x is None:
        return default
    if not isinstance(x, t.Iterable) or isinstance(x, str):
        return [x]
    elif isinstance(x, list):
        return x
    else:
        return list(x)


def enable_tracing(modules: t.List[str] = None):
    effective_modules = []
    for module in to_list(modules):
        if module == "machinery":
            effective_modules += ["eskema", "fastparquet", "frictionless", "fsspec", "pandas"]
        if module == "core":
            effective_modules += ["eskema"]
        else:
            effective_modules += [module]
    try:
        import hunter  # noqa: F401

        _enable_tracing(sorted(set(effective_modules)))
    except ImportError:
        logger.warning("Package `hunter` not installed")


def _enable_tracing(modules: t.List[str] = None):
    from hunter import Q, trace

    if not modules:
        return

    logger.info(f"Tracing modules {modules}")
    constraint = Q(module_startswith=modules[0])
    for module in modules[1:]:
        constraint = constraint | Q(module_startswith=module)
    trace(constraint)
