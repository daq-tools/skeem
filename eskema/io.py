import io
import logging
import typing as t
from collections import OrderedDict

import json_stream
import pandas as pd
from fsspec.implementations.local import LocalFileOpener
from fsspec.spec import AbstractBufferedFile
from json_stream.base import StreamingJSONList, StreamingJSONObject

from eskema.type import ContentType

logger = logging.getLogger(__name__)


BytesString = t.Union[bytes, str]
BytesStringList = t.List[BytesString]


def peek(data: t.IO[t.Any], content_type: t.Optional[ContentType], peek_bytes: int, peek_lines: int) -> t.BinaryIO:
    """
    Only peek at the first bytes/lines of data.
    """
    binary_files = [ContentType.XLSX, ContentType.ODS]

    # Only optionally seek to the file's beginning.
    # if hasattr(data, "seekable") and data.seekable():  # noqa: ERA001
    #     data.seek(0)  # noqa: ERA001

    if content_type in binary_files:
        logger.info(f"WARNING: Hitting a speed bump by needing to read file of type {binary_files} as a whole")
        return io.BytesIO(data.read())
    else:
        if content_type is ContentType.JSON:
            logger.info("WARNING: Hitting a speed bump by needing to read JSON document as a whole")
            payload = data.read()
        else:
            empty = ""
            if isinstance(data, io.BytesIO) or (hasattr(data, "mode") and "b" in data.mode):
                empty = b""  # type: ignore[assignment]

            # Optimize peek path for `fsspec`-based file systems.
            # TODO: Evaluate using the `smart-open` package.
            if isinstance(data, (AbstractBufferedFile, LocalFileOpener)):
                payload = fsspec_peek(data=data, empty=empty, peek_bytes=peek_bytes, peek_lines=peek_lines)
            else:
                payload = empty.join(data.readlines(peek_lines))  # type: ignore[arg-type]

        if isinstance(payload, str):
            payload = payload.encode()

        return io.BytesIO(payload)


def fsspec_peek(
    data: t.Union[io.IOBase, t.IO[t.Any]], peek_bytes: int, peek_lines: int, empty: BytesString
) -> BytesString:
    """
    Read into the file-like using an amount of bytes, instead of interrupting
    the line generator, because it turned out that `readlines()` interacting
    with `fsspec` still reads the whole file/stream.
    """
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


def read_lineprotocol(data: t.IO[t.Any]):
    """
    Read stream of InfluxDB line protocol and decode raw data.

    https://docs.influxdata.com/influxdb/latest/reference/syntax/line-protocol/
    """
    from line_protocol_parser import LineFormatError, parse_line

    for line in data.readlines():
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
