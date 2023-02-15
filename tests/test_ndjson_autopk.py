from click.testing import CliRunner

from eskema.autopk import infer_pk
from eskema.cli import cli
from eskema.type import ContentType
from eskema.util import sql_canonicalize
from tests.util import get_basic_sql_reference, random_table_name


def test_ndjson_autopk_easy_id():
    """
    To get started, this is an easy test case with data in NDJSON format.
    All columns starting with "id" or derivates will immediately be selected
    as primary key.
    """
    indata = """
{"Identifier":1,"name":"foo"}
{"Identifier":2,"name":"bar"}
    """.strip()
    assert infer_pk(indata, ContentType.NDJSON) == "Identifier"


def test_ndjson_autopk_easy_more():
    """
    There is another fixed set of primary candidates for primary keys,
    which must match equal.
    """
    indata = """
{"PK":1,"name":"foo"}
{"PK":2,"name":"bar"}
    """.strip()
    assert infer_pk(indata, ContentType.NDJSON) == "PK"


def test_ndjson_autopk_any_column_known():
    """
    The primary key is selected based on a fixed list of secondary candidates.
    """
    indata = """
{"name":"foo","Kennung":1}
{"name":"bar","Kennung":2}
    """.strip()
    assert infer_pk(indata, ContentType.NDJSON) == "Kennung"


def test_ndjson_autopk_first_column_unknown():
    """
    The primary key is selected from the first column a) because it is the
    first one, and b) its values are unique amongst the first 1000 records.
    This works with column names in any language.
    """
    indata = """
{"ідентифікатор":1,"name":"foo"}
{"ідентифікатор":2,"name":"bar"}
    """.strip()
    assert infer_pk(indata, ContentType.NDJSON) == "ідентифікатор"


def test_ndjson_autopk_undetected():
    """
    Proof that the first column does not get selected blindly on non-unique columns.

    When it's obvious that a column candidate's values are not unique, by
    looking at the first chunk of data, a primary key can not be derived.
    """
    indata = """
{"ідентифікатор":1,"name":"foo"}
{"ідентифікатор":2,"name":"bar"}
{"ідентифікатор":2,"name":"baz"}
    """.strip()
    assert infer_pk(indata, ContentType.NDJSON) is None


def test_ndjson_autopk_cli_file_without_primary_key(ndjson_file_basic):
    """
    CLI test: Primary key is derived from data.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(
        cli, f"infer-ddl --dialect=crate --table-name={table_name} {ndjson_file_basic}", catch_exceptions=False
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name)


def test_ndjson_autopk_cli_file_with_primary_key(ndjson_file_basic):
    """
    CLI test: Primary key takes precedence when obtained from the user.
    """
    table_name = random_table_name("foo")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        f"infer-ddl --dialect=crate --table-name={table_name} --primary-key=name {ndjson_file_basic}",
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert computed == get_basic_sql_reference(table_name=table_name, primary_key="name")
