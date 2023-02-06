import random
import textwrap
import typing as t
from pathlib import Path

from eskema.monkey import clean_key_name
from eskema.util import sql_canonicalize


def random_table_name(label: t.Union[Path, str]):
    name = label
    if isinstance(label, Path):
        name = label.name
    return f"eskema-test-{name}-{random.randint(1, 999)}"


def get_basic_sql_reference(table_name, primary_key="id"):
    """
    The reference how the inferred SQL should look like.
    """
    basic_reference = sql_canonicalize(
        textwrap.dedent(
            f"""
        CREATE TABLE "{clean_key_name(table_name)}" (
            "id" INT NOT NULL,
            "name" STRING NOT NULL,
            "date" TIMESTAMP,
            "fruits" STRING NOT NULL,
            "price" DOUBLE NOT NULL,
            PRIMARY KEY ("{primary_key}")
        );
    """
        )
    )
    return basic_reference.strip("\n")
