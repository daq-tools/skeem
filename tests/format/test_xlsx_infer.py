import pytest
from click.testing import CliRunner

from skeem.cli import cli
from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlResult, SqlTarget
from skeem.types import ContentType
from tests.util import BACKENDS, get_basic_sql_reference, get_basic_sql_reference_alt, getcmd


@pytest.mark.parametrize("backend", BACKENDS)
def test_xlsx_infer_library_success(xlsx_file_basic, backend: str):
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
        backend=backend,
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("url", ["xlsx_file_basic", "xlsx_url_basic"])
@pytest.mark.parametrize("backend", BACKENDS)
def test_xlsx_infer_url(request, url, backend: str):
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
def test_xlsx_infer_cli_file_without_tablename(xlsx_file_basic, backend: str):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, getcmd(xlsx_file_basic, backend=backend), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_xlsx_infer_cli_file_with_tablename(xlsx_file_basic, backend: str):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli, getcmd(xlsx_file_basic, more_args=f"--table-name={table_name}", backend=backend), catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_xlsx_infer_cli_file_with_sheet(xlsx_file_basic, backend: str):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "sheet2"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        getcmd(xlsx_file_basic, more_args=f"--table-name={table_name} --address=Sheet2", backend=backend),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference_alt(backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
@pytest.mark.parametrize("content_type", ["xlsx", ContentType.XLSX.value])
def test_xlsx_infer_cli_stdin_with_content_type(xlsx_file_basic, content_type: str, backend: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=getcmd(more_args=f"--table-name={table_name} --content-type={content_type} -", backend=backend),
        input=open(xlsx_file_basic, "rb"),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference
