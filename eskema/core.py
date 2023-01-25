import io
import logging
import typing as t
from pathlib import Path

from eskema import monkey

monkey.activate()

from ddlgenerator.ddlgenerator import Table

BYTES_MAGIC = 1000


def generate_ddl(tbl, table_name=None, primary_key=None):
    """
    Prints code (SQL, SQLAlchemy, etc.) to define a table.
    """
    table = Table(
        tbl,
        table_name=table_name,
        varying_length_text=True,
        uniques=False,
        pk_name=primary_key,
        force_pk=False,
        reorder=False,
        loglevel=logging.DEBUG,
        limit=None,
    )
    return table.sql(dialect="crate", creates=True, drops=False, inserts=False)


def get_firstline(filepath: t.Union[Path, str, t.IO]):
    if isinstance(filepath, io.TextIOBase):
        return stream_get_firstline(filepath)
    elif isinstance(filepath, (Path, str)):
        filepath = Path(filepath)
        with open(filepath, "r") as f:
            return stream_get_firstline(f)


def stream_get_firstline(stream: t.IO):
    firstline = stream.readline()
    return io.StringIO(firstline)
