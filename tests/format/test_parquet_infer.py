import pytest
from click.testing import CliRunner

from skeem.cli import cli
from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlResult, SqlTarget
from tests.util import get_basic_sql_reference, getcmd

BACKEND = "frictionless"


def test_parquet_infer_library_success(parquet_file_basic):
    """
    Verify basic library use.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            path=parquet_file_basic,
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=BACKEND)
    assert computed == reference


@pytest.mark.parametrize("url", ["parquet_file_basic", "parquet_url_basic"])
def test_parquet_infer_url(request, url):
    """
    CLI test: Table name is correctly derived from the input file or URL.
    """

    url = request.getfixturevalue(url)

    runner = CliRunner()
    result = runner.invoke(cli, getcmd(url, backend=BACKEND), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=BACKEND)
    assert computed == reference


def test_parquet_infer_cli_file_without_tablename(parquet_file_basic):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, getcmd(parquet_file_basic, backend=BACKEND), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=BACKEND)
    assert computed == reference


def test_parquet_infer_cli_file_with_tablename(parquet_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli, getcmd(parquet_file_basic, more_args=f"--table-name={table_name}", backend=BACKEND), catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=BACKEND)
    assert computed == reference
