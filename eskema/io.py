import logging
import typing as t

logger = logging.getLogger(__name__)


BytesString = t.Union[bytes, str]
BytesStringList = t.List[BytesString]


def fsspec_peek(data: t.IO[t.Any], peek_bytes: int, peek_lines: int, empty: BytesString) -> BytesString:
    """
    Read into the file-like using an amount of bytes, instead of interrupting
    the line generator, because it turned out that `readlines()` interacting
    with `fsspec` still reads the whole file/stream.
    """
    logger.info(f"Reading {peek_bytes} bytes")

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
