import io

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import PEEK_BYTES, Resource, SqlResult, SqlTarget
from tests.util import BACKENDS, get_basic_sql_reference, getcmd


@pytest.fixture
def basic_stream_csv():
    """
    A stream of input data. Here, in CSV format.
    """
    return io.StringIO(
        """
id,name,date,fruits,price
1,"foo","2014-10-31T09:22:56","apple,banana",0.42
2,"bar",,"pear",0.84
    """.lstrip()
    )


@pytest.mark.parametrize("backend", BACKENDS)
def test_csv_infer_library_success(basic_stream_csv, backend: str):
    """
    Verify basic library use.
    """
    table_name = "foo"
    sg = SchemaGenerator(
        resource=Resource(
            data=basic_stream_csv,
            content_type="csv",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
        backend=backend,
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name=table_name, primary_key_is_string=True, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_csv_infer_cli_file_without_tablename(csv_file_basic, backend: str):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, getcmd(csv_file_basic, backend=backend), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic", backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
def test_csv_infer_cli_file_with_tablename(csv_file_basic, backend: str):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli, getcmd(csv_file_basic, more_args=f"--table-name={table_name}", backend=backend), catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, backend=backend)
    assert computed == reference


@pytest.mark.parametrize("backend", BACKENDS)
@pytest.mark.parametrize("content_type", ["csv", "text/csv"])
def test_csv_infer_cli_stdin_with_content_type(basic_stream_csv, content_type: str, backend: str):
    """
    CLI test: Read data from stdin.
    """
    table_name = "foo"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=getcmd(more_args=f"--table-name={table_name} --content-type={content_type} -", backend=backend),
        input=basic_stream_csv.read(PEEK_BYTES),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name, primary_key_is_string=True, backend=backend)
    assert computed == reference
