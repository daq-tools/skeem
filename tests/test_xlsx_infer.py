import textwrap

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.type import ContentType
from tests.util import get_basic_sql_reference


def test_xlsx_infer_library_success(xlsx_file_basic):
    """
    Verify basic library use.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            data=None,
            path=xlsx_file_basic,
            content_type="xlsx",
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


def test_xlsx_infer_cli_file_without_tablename(xlsx_file_basic):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate {xlsx_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic")
    assert computed == reference


def test_xlsx_infer_cli_file_with_tablename(xlsx_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate --table-name={table_name} {xlsx_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference


def test_xlsx_infer_cli_file_with_sheet(xlsx_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "sheet2"

    runner = CliRunner()
    result = runner.invoke(
        cli, f"infer-ddl --dialect=crate --table-name={table_name} {xlsx_file_basic} --address=Sheet2"
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert (
        computed
        == textwrap.dedent(
            """
    CREATE TABLE "sheet2" (
        "foo" DOUBLE NOT NULL,
        "bar" DOUBLE NOT NULL
    );
    """
        ).strip()
    )


@pytest.mark.parametrize("content_type", ["xlsx", ContentType.XLSX.value])
def test_xlsx_infer_cli_stdin_with_content_type(xlsx_file_basic, content_type: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=f"infer-ddl --dialect=crate --table-name={table_name} --content-type={content_type} -",
        input=open(xlsx_file_basic, "rb"),
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference