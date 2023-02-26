import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.settings import PEEK_BYTES
from tests.util import BACKENDS, get_basic_sql_reference, getcmd


@pytest.mark.parametrize("backend", BACKENDS)
def test_ndjson_infer_library_stream(ndjson_stream_basic, backend: str):
    """
    Verify library use with an input stream.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            data=ndjson_stream_basic,
            content_type="ndjson",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
        backend=backend,
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


def test_ndjson_infer_library_url_github(ndjson_github_url_basic):
    """
    Verify library use with an input URL.
    """
    table_name = "foo"
    backend = "ddlgen"
    sg = SchemaGenerator(
        resource=Resource(
            path=ndjson_github_url_basic,
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
        ),
        backend=backend,
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("url", ["ndjson_file_basic", "ndjson_url_basic"])
@pytest.mark.parametrize("backend", BACKENDS)
def test_ndjson_infer_url(request, url, backend: str):
    """
    CLI test: Table name is correctly derived from the input file or URL.
    """

    url = request.getfixturevalue(url)

    runner = CliRunner()
    result = runner.invoke(cli, getcmd(url, backend=backend), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_ndjson_infer_cli_file_without_tablename(ndjson_file_basic, backend: str):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, getcmd(ndjson_file_basic, backend=backend), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_ndjson_infer_cli_file_with_tablename(ndjson_file_basic, backend: str):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli, getcmd(ndjson_file_basic, more_args=f"--table-name={table_name}", backend=backend), catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
@pytest.mark.parametrize("content_type", ["ndjson", "jsonl", "application/x-ldjson"])
def test_ndjson_infer_cli_stdin_with_content_type(ndjson_stream_basic, content_type: str, backend: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=getcmd(more_args=f"--table-name={table_name} --content-type={content_type} -", backend=backend),
        input=ndjson_stream_basic.read(PEEK_BYTES),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference
