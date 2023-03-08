import random
import textwrap
import typing as t
from pathlib import Path

from ddlgenerator.reshape import clean_key_name

from skeem.util.sql import sql_canonicalize

BACKENDS = ["ddlgen", "frictionless"]


def random_table_name(label: t.Union[Path, str]):
    name = label
    if isinstance(label, Path):
        name = label.name
    return f"skeem-test-{name}-{random.randint(1, 9999)}"


def get_basic_sql_reference(
    table_name,
    primary_key="id",
    timestamp_not_null: bool = False,
    timestamp_is_string: bool = False,
    backend: str = "ddlgen",
):
    """
    The reference how the inferred SQL should look like.
    """
    if backend == "ddlgen":
        ddl = f"""
    CREATE TABLE "{clean_key_name(table_name)}" (
        "id" INT NOT NULL,
        "name" STRING NOT NULL,
        "date" TIMESTAMP{" NOT NULL" if timestamp_not_null else ""},
        "fruits" STRING NOT NULL,
        "price" DOUBLE NOT NULL,
        PRIMARY KEY ("{primary_key}")
    );
    """
    elif backend == "frictionless":
        ddl = f"""
    CREATE TABLE {clean_key_name(table_name)} (
        id INT NOT NULL,
        name STRING,
        date {"TIMESTAMP" if not timestamp_is_string else "STRING"}{" NOT NULL" if timestamp_not_null else ""},
        fruits STRING,
        price FLOAT,
        PRIMARY KEY ({primary_key})
    );
    """
    else:
        raise ValueError(f"Unknown SQL DDL backend: {backend}")
    return sql_canonicalize(textwrap.dedent(ddl)).strip("\n")


def get_basic_sql_reference_alt(backend: str) -> str:
    if backend == "ddlgen":
        ddl = """
        CREATE TABLE "sheet2" (
            "foo" DOUBLE NOT NULL,
            "bar" DOUBLE NOT NULL
        );
        """
    elif backend == "frictionless":
        ddl = """
        CREATE TABLE sheet2 (
            foo FLOAT,
            bar FLOAT
        );
        """
    return textwrap.dedent(ddl).strip()


def getcmd(
    filename: t.Optional[str] = None, more_args: t.Optional[str] = None, dialect: str = "crate", backend: str = "ddlgen"
) -> str:
    cmd = f"infer-ddl --dialect={dialect} --backend={backend}"
    if filename is not None:
        cmd += f" {filename}"
    if more_args is not None:
        cmd += f" {more_args}"
    return cmd
