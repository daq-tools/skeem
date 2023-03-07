import io
import json
import textwrap
import typing as t
from pathlib import Path


def jd(data: t.Any):
    """
    Pretty-print JSON with indentation.
    """
    print(json.dumps(data, indent=2))  # noqa: T201


def enum_values(enum):
    items = []
    for item in enum:
        items.append(item.value)
    return items


def unwrap(value: str):
    return textwrap.dedent(value).strip()


def to_bytes(payload: t.Union[str, bytes], name: t.Optional[str] = None) -> io.BytesIO:
    if isinstance(payload, str):
        payload = payload.encode()
    data = io.BytesIO(payload)
    data.name = name or "UNKNOWN"
    return data


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


def head(fp: t.IO, n: int = None, c: int = None):
    """
    head -- display first lines of a file, implemented as a generator.

    TODO: Implement the `keepends` options, like `splitlines`.
    """
    """
    HEAD(1)                   BSD General Commands Manual                  HEAD(1)

    NAME
         head -- display first lines of a file

    SYNOPSIS
         head [-n count | -c bytes] [file ...]

    DESCRIPTION
         This filter displays the first count lines or bytes of each of the specified files,
         or of the standard input if no files are specified. If count is omitted it defaults to 10.

         If more than a single file is specified, each file is preceded by a header consisting of
         the string ``==> XXX <=='' where ``XXX'' is the name of the file.

    EXIT STATUS
         The head utility exits 0 on success, and >0 if an error occurs.

    SEE ALSO
         tail(1)

    HISTORY
         The head command appeared in PWB UNIX.

    BSD                              June 6, 1993                              BSD
    """
    if n is not None and c is not None:
        raise ValueError("head: can't combine line and byte counts")

    if c is not None:
        yield fp.read(c)
        return

    # Default value.
    n = n or 10

    # TODO: Review: Does it properly split lines, and lazily read the file?
    # https://web.physics.utah.edu/~detar/lessons/python/fileio_formatting/node11.html
    for line in fp:
        yield line
        n -= 1
        if n <= 0:
            break
