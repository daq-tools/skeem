import io
import textwrap

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import BYTES_MAGIC, generate_ddl, get_firstline
from eskema.util import sql_canonicalize


def get_basic_sql_reference(table_name):
    """
    The reference how the inferred SQL should look like.
    """
    basic_reference = sql_canonicalize(
        textwrap.dedent(
            """
        CREATE TABLE "{table_name}" (
            "id" INT NOT NULL,
            "name" STRING NOT NULL,
            "date" TIMESTAMP NOT NULL,
            "fruits" STRING NOT NULL,
            "price" DOUBLE NOT NULL,
            PRIMARY KEY ("id")
        );
    """
        )
    )
    return basic_reference.strip("\n").format(table_name=table_name)


@pytest.fixture
def basic_stream_ndjson():
    """
    A stream of input data. Here, in ndjson format, aka. jsonl.

    http://ndjson.org/
    """
    return io.StringIO(
        """
{"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
{"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
    """.lstrip()
    )


def test_ndjson_infer_library(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    firstline = get_firstline(basic_stream_ndjson)
    sql = generate_ddl(firstline, table_name="foo1", primary_key="id")
    computed = sql_canonicalize(sql)
    assert computed == get_basic_sql_reference(table_name="foo1")


def test_ndjson_infer_cli_file_without_tablename(basic_stream_ndjson):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, "infer-ddl --dialect=crate tests/basic.ndjson")
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name="basic")


def test_ndjson_infer_cli_file_with_tablename(basic_stream_ndjson):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    runner = CliRunner()
    result = runner.invoke(cli, "infer-ddl --dialect=crate --table-name=foo2 tests/basic.ndjson")
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name="foo2")


def test_ndjson_infer_json_cli_stdin(basic_stream_ndjson):
    """
    CLI test: Read data from stdin.
    """
    runner = CliRunner()
    result = runner.invoke(
        cli, args="infer-ddl --dialect=crate --table-name=foo3 -", input=basic_stream_ndjson.read(BYTES_MAGIC)
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name="foo3")
