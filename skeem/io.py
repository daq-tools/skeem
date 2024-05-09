import io
import logging
import tempfile
import typing as t
from collections import OrderedDict
from pathlib import Path

import fsspec
import pandas as pd
from fsspec.implementations.local import LocalFileOpener
from fsspec.spec import AbstractBufferedFile

from skeem.settings import PEEK_BYTES, PEEK_LINES
from skeem.type import ContentType, ContentTypeGroup

if t.TYPE_CHECKING:
    import xarray


logger = logging.getLogger(__name__)


BytesString = t.Union[bytes, str]
BytesStringList = t.List[BytesString]


def open(path: t.Union[Path, str]):  # noqa: A001
    """
    Access a plethora of resources using `fsspec`.
    """
    path = str(path)
    kwargs: t.Dict[str, t.Any] = {}
    if path.startswith("s3"):
        kwargs["anon"] = True

    # TODO: Why isn't compression selected transparently?
    if path.endswith(".gz"):
        kwargs["compression"] = "gzip"
    fs = fsspec.open(path, mode="rb", **kwargs).open()
    return fs


def peek(
    data: t.IO[t.Any], content_type: t.Optional[ContentType] = None, peek_bytes: int = None, peek_lines: int = None
) -> t.IO:
    """
    Only peek at the first bytes/lines of data.
    """

    # Only optionally seek to the file's beginning.
    # if hasattr(data, "seekable") and data.seekable():  # noqa: ERA001
    #     data.seek(0)  # noqa: ERA001

    if content_type in ContentTypeGroup.NO_PARTIAL:
        logger.info(f"WARNING: Hitting a speed bump by needing to read file of type {content_type} as a whole")
        return io.BytesIO(data.read())
    else:
        if content_type is ContentType.JSON:
            logger.info("WARNING: Hitting a speed bump by needing to read JSON document as a whole")
            payload = data.read()
        else:
            empty: t.Union[bytes, str]
            is_binary = False
            if hasattr(data, "mode"):
                if isinstance(data.mode, str):
                    is_binary = "b" in data.mode
                elif isinstance(data.mode, int):
                    is_binary = data.mode == 1
                else:
                    raise ValueError(f"Unsupported type for data.mode={data.mode}, type={type(data.mode)}")
            if isinstance(data, io.BytesIO) or is_binary:
                empty = b""  # type: ignore[assignment]
            else:
                empty = ""

                # Optimize peek path for `fsspec`-based file systems.
            # TODO: Evaluate using the `smart-open` package.
            if isinstance(data, (AbstractBufferedFile, LocalFileOpener)):
                payload = fsspec_peek(data=data, empty=empty, peek_bytes=peek_bytes, peek_lines=peek_lines)
            elif isinstance(data, (bytes, str)):
                payload = data
            elif hasattr(data, "readlines"):
                # https://lwn.net/Articles/816415/
                payload = empty.join(data.readlines(peek_bytes))  # type: ignore[arg-type]
            else:
                raise TypeError(f"No method for peeking at data, type={type(data).__name__}")

        if isinstance(payload, str):
            payload = payload.encode()

        return io.BytesIO(payload)


def fsspec_peek(
    data: t.Union[io.IOBase, t.IO[t.Any]], empty: BytesString, peek_bytes: int = None, peek_lines: int = None
) -> BytesString:
    """
    Read into the file-like using an amount of bytes, instead of interrupting
    the line generator, because it turned out that `readlines()` interacting
    with `fsspec` still reads the whole file/stream.

    TODO: Refactor "partial-reading-with-line-coherence" into generic function.
    """

    # Default values.
    peek_bytes = peek_bytes or -1

    logger.info(f"Reading max. {peek_bytes} bytes")

    # Read by amount of bytes, and split lines.
    payload = data.read(peek_bytes)
    lines = payload.splitlines(keepends=True)

    # Determine if it was a partial read.
    more_data = data.read(1)
    is_partial_read = more_data != "" and more_data != b""

    # Strip last line, only if it is incomplete.
    if is_partial_read:
        lines = strip_incomplete_line(lines)

    # Trim to requested amount of lines.
    lines = lines[:peek_lines]
    logger.info(f"Received {len(lines)} lines")

    # Return payload.
    payload = empty.join(lines)
    return payload


def dataset_to_dataframe(
    ds: "xarray.Dataset",
    peek_lines: int,
) -> pd.DataFrame:
    logger.info(f"Dataset:\n{ds}")
    df = ds.to_dataframe().dropna()
    logger.debug(f"DataFrame:\n{df}")
    logger.info(f"Reading {peek_lines} records of `xarray.Dataset`")
    df = df[:peek_lines]
    df = df.reset_index()
    return df


def strip_incomplete_line(lines: BytesStringList) -> BytesStringList:
    """
    Strip last line, only if it is incomplete.
    """
    last_line = lines[-1]
    last_line_ends_with_newline = (isinstance(last_line, str) and last_line.endswith("\n")) or (
        isinstance(last_line, bytes) and last_line.endswith(b"\n")
    )
    if not last_line_ends_with_newline:
        lines = lines[:-1]
    return lines


def json_get_first_records(
    data: t.Union[t.IO, t.Iterable], nrecords: int = 5
) -> t.List[t.OrderedDict[t.AnyStr, t.Any]]:
    """
    Read JSON data lazily, without loading the whole document into memory.

    - From a "list of objects" JSON document, get only the first N records.
    - From a "single object" JSON document, get only the first record.

    TODO: Raise from nrecords=5 to nrecords=100?
    """
    import json_stream
    from json_stream.base import StreamingJSONList, StreamingJSONObject

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


def read_lineprotocol(data: t.IO[t.Any]):
    """
    Read stream of InfluxDB line protocol and decode raw data.

    https://docs.influxdata.com/influxdb/latest/reference/syntax/line-protocol/
    """
    from line_protocol_parser import LineFormatError, parse_line

    for line in data.readlines(PEEK_BYTES):
        try:
            yield parse_line(line)
        except LineFormatError as ex:
            logger.info(f"WARNING: Line protocol item {line} invalid. Reason: {ex}")


def records_from_lineprotocol(data: t.IO[t.Any]):
    """
    Read stream of InfluxDB line protocol and generate `OrderedDict` records.
    """
    for lp in read_lineprotocol(data=data):
        record = OrderedDict()
        record["time"] = lp["time"]
        for tag, value in lp["tags"].items():
            record[tag] = value
        for field, value in lp["fields"].items():
            record[field] = value
        yield record


def dataframe_from_lineprotocol(data: t.IO[t.Any]):
    """
    Read stream of InfluxDB line protocol into pandas DataFrame.
    """
    records = records_from_lineprotocol(data)
    return pd.DataFrame(records)


def to_tempfile(data: t.IO[t.Any], suffix: t.Optional[str] = None) -> t.IO:
    """
    Write a buffer to a temporary file.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=suffix)
    tmp.write(data.read())
    tmp.seek(0)
    return tmp


def to_dataframe(data: t.Union[t.IO], content_type: ContentType, address: t.Any = None) -> pd.DataFrame:
    """
    Converge data to pandas DataFrame, trying to peek at the first lines/records of data only.

    This machinery is currently used by `skeem.autopk`.
    """

    if data is None:
        raise ValueError("Unable to operate on empty data")

    # Sanity checks.
    if not isinstance(content_type, ContentType):
        raise TypeError(
            f"Failed to infer primary key with invalid content type "
            f"(value={content_type}, type={type(content_type).__name__}), "
            f"expected `ContentType`"
        )

    if content_type is ContentType.CSV:
        df = pd.read_csv(data, nrows=PEEK_LINES)

    # Only load the first record(s) from a regular JSON document.
    elif content_type is ContentType.JSON:
        records = json_get_first_records(data, nrecords=PEEK_LINES)
        df = pd.DataFrame.from_records(data=records)

    elif content_type is ContentType.LINEPROTOCOL:
        # TODO: Review: No `PEEK_LINES` is used here?
        df = dataframe_from_lineprotocol(data=data)

    elif content_type.is_ndjson():
        df = pd.read_json(data, lines=True, nrows=PEEK_LINES)

    elif content_type in [ContentType.ODS, ContentType.XLSX]:
        sheet_name = address or 0
        df = pd.read_excel(data, sheet_name=sheet_name, nrows=PEEK_LINES)

    else:
        raise ValueError(f"Unable to process content type: {content_type}")

    return df
