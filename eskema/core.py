import io
import logging

from eskema import monkey

monkey.activate()

from ddlgenerator.ddlgenerator import Table


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


def file_get_firstline(filepath):
    with open(filepath, "r") as f:
        firstline = f.readline()
        return io.StringIO(firstline)
