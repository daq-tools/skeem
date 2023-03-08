import pytest
from click.testing import CliRunner

from skeem.cli import cli
from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlResult, SqlTarget
from skeem.util.data import unwrap
from tests.util import getcmd

reference = unwrap(
    """
CREATE TABLE "aircraft_track_lear" (
    "time" TIMESTAMP NOT NULL,
    "altitude" DOUBLE NOT NULL,
    "latitude" DOUBLE NOT NULL,
    "longitude" DOUBLE NOT NULL,
    "pressure" DOUBLE NOT NULL,
    "tdry" DOUBLE NOT NULL,
    "dp" DOUBLE NOT NULL,
    "mr" DOUBLE NOT NULL,
    "wspd" DOUBLE NOT NULL,
    "wdir" DOUBLE NOT NULL,
    "drops" DOUBLE NOT NULL
);
    """
)


def test_netcdf_infer_library_success(netcdf_file_aircraft):
    """
    Verify basic library use.
    """
    sg = SchemaGenerator(
        resource=Resource(path=netcdf_file_aircraft),
        target=SqlTarget(dialect="crate"),
    )

    computed = sg.to_sql_ddl().canonical
    assert computed == reference


@pytest.mark.parametrize("url", ["netcdf_file_aircraft", "netcdf_url_aircraft"])
def test_netcdf_infer_url(request, url):
    """
    CLI test: Table name is correctly derived from the input file or URL.
    """
    backend = "ddlgen"

    url = request.getfixturevalue(url)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        getcmd(url, dialect="crate", backend=backend),
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert computed == reference
