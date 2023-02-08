from click.testing import CliRunner

from eskema.cli import cli
from eskema.util import sql_canonicalize
from tests.util import get_basic_sql_reference, random_table_name


def test_xlsx_autopk_cli_file_without_primary_key(xlsx_file_basic):
    """
    CLI test: Primary key is derived from data.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate --table-name={table_name} {xlsx_file_basic}")
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name)


def test_xlsx_autopk_cli_file_with_primary_key(xlsx_file_basic):
    """
    CLI test: Primary key takes precedence when obtained from the user.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(
        cli, f"infer-ddl --dialect=crate --table-name={table_name} --primary-key=name {xlsx_file_basic}"
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name, primary_key="name")
