import io

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import PEEK_BYTES, Resource, SqlResult, SqlTarget
from tests.util import get_basic_sql_reference


@pytest.fixture
def basic_stream_ndjson():
    """
    A stream of input data. Here, in NDJSON (ex. LDJSON) format, aka. JSON Lines.

    http://ndjson.org/
    """
    return io.StringIO(
        """
{"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
{"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
    """.lstrip()
    )


def test_ndjson_infer_library_success(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            data=basic_stream_ndjson,
            content_type="ndjson",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference


def test_ndjson_infer_cli_file_without_tablename(ndjson_file_basic):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate {ndjson_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic")
    assert computed == reference


def test_ndjson_infer_cli_file_with_tablename(ndjson_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate --table-name={table_name} {ndjson_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference


@pytest.mark.parametrize("content_type", ["ndjson", "jsonl", "application/x-ldjson"])
def test_ndjson_infer_cli_stdin_with_content_type(basic_stream_ndjson, content_type: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=f"infer-ddl --dialect=crate --table-name={table_name} --content-type={content_type} -",
        input=basic_stream_ndjson.read(PEEK_BYTES),
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference
