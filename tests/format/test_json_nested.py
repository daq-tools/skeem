import textwrap

import pytest
from click.testing import CliRunner

from skeem.cli import cli
from skeem.model import SqlResult
from tests.util import getcmd

reference = textwrap.dedent(
    """
CREATE TABLE "basic_nested" (
    "id" TEXT NOT NULL,
    "submitter" TEXT NOT NULL,
    "authors" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "comments" TEXT NOT NULL,
    "journal_ref" TEXT NOT NULL,
    "doi" TEXT NOT NULL,
    "report_no" TEXT NOT NULL,
    "categories" TEXT NOT NULL,
    "license" TEXT,
    "abstract" TEXT NOT NULL,
    "update_date" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY ("id")
);


CREATE TABLE "versions" (
    "version" TEXT NOT NULL,
    "created" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    "basic_nested_id" TEXT NOT NULL,
    FOREIGN KEY("basic_nested_id") REFERENCES "basic_nested" ("id")
);
    """
).strip()


def test_json_nested_infer_cli_file(json_nested_file_basic):
    """
    Test a nested JSON document.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=postgresql {json_nested_file_basic}", catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert computed == reference


@pytest.mark.parametrize("url", ["json_nested_file_basic", "json_nested_url_basic"])
def test_json_nested_infer_url(request, url):
    """
    CLI test: Table name is correctly derived from the input file or URL.
    """
    backend = "ddlgen"

    url = request.getfixturevalue(url)

    runner = CliRunner()
    result = runner.invoke(cli, getcmd(url, dialect="postgresql", backend=backend), catch_exceptions=False)
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    assert computed == reference
