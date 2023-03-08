import pytest
from click.testing import CliRunner

from skeem.cli import cli
from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlResult, SqlTarget
from tests.util import get_basic_sql_reference, get_basic_sql_reference_alt, getcmd

GSHEET_URL_SHEET_BASIC = "https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view"
GSHEET_URL_SHEET_SHEET2 = (
    "https://docs.google.com/spreadsheets/d/1ExyrawjlyksbC6DOM6nLolJDbU8qiRrrhxSuxf5ScB0/view#gid=883324548"
)
BACKEND = "frictionless"

pytestmark = pytest.mark.slow


def test_gsheet_infer_library_success():
    """
    Verify basic library use.
    """

    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            path=GSHEET_URL_SHEET_BASIC,
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
        backend=BACKEND,
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, timestamp_is_string=True, backend=BACKEND)
    assert computed == reference


def test_gsheet_infer_cli_file_without_tablename():
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, getcmd(GSHEET_URL_SHEET_BASIC, backend=BACKEND), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="VIEW", timestamp_is_string=True, backend=BACKEND)
    assert computed == reference


def test_gsheet_infer_cli_file_with_tablename():
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        getcmd(GSHEET_URL_SHEET_BASIC, more_args=f"--table-name={table_name}", backend=BACKEND),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, timestamp_is_string=True, backend=BACKEND)
    assert computed == reference


def test_gsheet_infer_cli_file_with_sheet():
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "sheet2"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        # TODO: Make option `--address="Sheet2"` work, instead of using `GSHEET_URL_SHEET_SHEET2`.
        getcmd(GSHEET_URL_SHEET_SHEET2, more_args=f"--table-name={table_name}", backend=BACKEND),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference_alt(BACKEND)
    assert computed == reference
