import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.util import unwrap
from tests.util import getcmd

reference = unwrap(
    """
CREATE TABLE "basic_lp" (
    "time" BIGINT NOT NULL,
    "fruits" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "id" SERIAL NOT NULL,
    "price" DECIMAL(2, 2) NOT NULL,
    PRIMARY KEY ("id")
);
    """
)

reference_irregular = unwrap(
    """
CREATE TABLE "irregular_lp" (
    "time" LONG NOT NULL,
    "sensor_id" STRING NOT NULL,
    "co" DOUBLE NOT NULL,
    "humidity" DOUBLE NOT NULL,
    "temperature" DOUBLE NOT NULL,
    "tag_foo" STRING,
    "val_more" DOUBLE
);
    """
)


def test_lineprotocol_infer_library_success(line_protocol_file_irregular):
    """
    Verify basic library use.
    """
    table_name = "irregular_lp"
    sg = SchemaGenerator(
        resource=Resource(
            path=line_protocol_file_irregular,
            content_type="lineprotocol",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name=table_name,
            primary_key="id",
        ),
        backend="ddlgen",
    )

    computed = sg.to_sql_ddl().canonical
    assert computed == reference_irregular


def test_lineprotocol_infer_cli_file(line_protocol_file_basic):
    """
    Test a nested JSON document.
    """
    runner = CliRunner()
    result = runner.invoke(
        cli, f"infer-ddl --dialect=postgresql --table-name=basic_lp {line_protocol_file_basic}", catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert computed == reference


@pytest.mark.parametrize("url", ["line_protocol_file_basic", "line_protocol_url_basic"])
def test_lineprotocol_infer_url(request, url):
    """
    CLI test: Table name is correctly derived from the input file or URL.
    """
    backend = "ddlgen"

    url = request.getfixturevalue(url)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        getcmd(url, dialect="postgresql", backend=backend, more_args="--table-name=basic_lp"),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert computed == reference
