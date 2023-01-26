import io
import logging
import typing as t
from pathlib import Path

from eskema import monkey
from eskema.autopk import infer_pk

monkey.activate()

from ddlgenerator.ddlgenerator import Table

BYTES_MAGIC = 1000


def generate_ddl(indata, table_name=None, primary_key=None):
    """
    Prints code (SQL, SQLAlchemy, etc.) to define a table.
    """

    indata = indata.read(10000)

    # When primary key is not given, try to infer it.
    if primary_key is None:
        primary_key = infer_pk(indata)

    firstline = get_firstline(indata)
    table = Table(
        firstline,
        table_name=table_name,
        varying_length_text=True,
        uniques=False,
        pk_name=primary_key,
        force_pk=True,
        reorder=False,
        loglevel=logging.DEBUG,
        limit=None,
    )
    return table.sql(dialect="crate", creates=True, drops=False, inserts=False)


def get_firstline(data: t.Union[Path, str, t.IO]):
    if isinstance(data, io.TextIOBase):
        return stream_get_firstline(data)
    elif isinstance(data, Path):
        data = Path(data)
        with open(data, "r") as f:
            return stream_get_firstline(f)
    elif isinstance(data, str):
        return io.StringIO(data.splitlines()[0])
    else:
        raise TypeError(f"Unable to decode identification chunk from type {type(data)}")


def stream_get_firstline(stream: t.Union[t.IO, str]):
    firstline = stream.readline()
    return io.StringIO(firstline)
