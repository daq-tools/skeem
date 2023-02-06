import io

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import PEEK_BYTES, Resource, SqlResult, SqlTarget
from tests.util import get_basic_sql_reference


@pytest.fixture
def basic_stream_json_document():
    """
    A stream of input data. Here, in JSON (document) format.
    """
    return io.StringIO(
        """
{
  "id": 1,
  "name": "foo",
  "date": "2014-10-31T09:22:56",
  "fruits": "apple,banana",
  "price": 0.42
}
    """.lstrip()
    )


def test_json_records_infer_library_success(basic_stream_json_document):
    """
    Verify basic library use.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            data=basic_stream_json_document,
            content_type="json",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, timestamp_not_null=True)
    assert computed == reference


def test_json_records_infer_cli_file_without_tablename(json_document_file_basic):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate {json_document_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic_document", timestamp_not_null=True)
    assert computed == reference


def test_json_records_infer_cli_file_with_tablename(json_document_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate --table-name={table_name} {json_document_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, timestamp_not_null=True)
    assert computed == reference


@pytest.mark.parametrize("content_type", ["json", "application/json"])
def test_json_records_infer_cli_stdin_with_content_type(basic_stream_json_document, content_type: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=f"infer-ddl --dialect=crate --table-name={table_name} --content-type={content_type} -",
        input=basic_stream_json_document.read(PEEK_BYTES),
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, timestamp_not_null=True)
    assert computed == reference
