from click.testing import CliRunner

from skeem.autopk import infer_pk
from skeem.cli import cli
from skeem.types import ContentType
from skeem.util.sql import sql_canonicalize
from tests.util import get_basic_sql_reference, random_table_name


def test_json_document_autopk_easy_id():
    """
    To get started, this is an easy test case with data in JSON (document) format.
    All columns starting with "id" or derivates will immediately be selected
    as primary key.
    """
    indata = """
{"Identifier":1,"name":"foo"}
    """.strip()
    assert infer_pk(indata, ContentType.JSON) == "Identifier"


def test_json_document_autopk_easy_more():
    """
    There is another fixed set of primary candidates for primary keys,
    which must match equal.
    """
    indata = """
{"PK":1,"name":"foo"}
    """.strip()
    assert infer_pk(indata, ContentType.JSON) == "PK"


def test_json_document_autopk_any_column_known():
    """
    The primary key is selected based on a fixed list of secondary candidates.
    """
    indata = """
{"name":"foo","Kennung":1},
    """.strip()
    assert infer_pk(indata, ContentType.JSON) == "Kennung"


def test_json_document_autopk_first_column_unknown():
    """
    The primary key is selected from the first column a) because it is the
    first one, and b) its values are unique amongst the first 1000 records.
    This works with column names in any language.
    """
    indata = """
{"ідентифікатор":1,"name":"foo"},
    """.strip()
    assert infer_pk(indata, ContentType.JSON) == "ідентифікатор"


def test_json_document_autopk_cli_file_without_primary_key(json_document_file_basic):
    """
    CLI test: Primary key is derived from data.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(
        cli, f"infer-ddl --dialect=crate --table-name={table_name} {json_document_file_basic}", catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name, timestamp_not_null=True)


def test_json_document_autopk_cli_file_with_primary_key(json_document_file_basic):
    """
    CLI test: Primary key takes precedence when obtained from the user.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        f"infer-ddl --dialect=crate --table-name={table_name} --primary-key=name {json_document_file_basic}",
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name, primary_key="name", timestamp_not_null=True)
