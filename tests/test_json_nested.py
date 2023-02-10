import textwrap

from click.testing import CliRunner

from eskema.cli import cli
from eskema.model import SqlResult


def test_json_nested_infer_cli_file(json_nested_file_basic):
    """
    Test a nested JSON document.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=postgresql {json_nested_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
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
    assert computed == reference
