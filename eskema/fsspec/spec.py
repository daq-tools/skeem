import typing as t


def readlines(fp: t.IO, nlines: int = None):
    """
    Improved version of `fsspec`'s `readline` method to
    support reading a limited amount of lines.
    """
    lines: t.List[t.Union[str, bytes]] = []
    for line in fp:
        yield line
        if nlines is not None:
            nlines -= 1
            if nlines <= 0:
                break
    return lines
