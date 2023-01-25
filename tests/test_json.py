import io
import textwrap

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import generate_ddl, get_firstline
from eskema.util import sql_canonicalize


def get_basic_sql_reference(table_name):
    """
    How the produced SQL should look like.
    """
    basic_reference = sql_canonicalize(
        textwrap.dedent(
            """
        CREATE TABLE "{table_name}" (
            "id" INT NOT NULL,
            "name" STRING NOT NULL,
            "date" TIMESTAMP NOT NULL,
            "fruits" STRING NOT NULL,
            "price" DOUBLE NOT NULL,
            PRIMARY KEY ("id")
        );
    """
        )
    )
    return basic_reference.strip("\n").format(table_name=table_name)


@pytest.fixture
def basic_stream_ndjson():
    return io.StringIO(
        """
{"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
{"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
    """.lstrip()
    )


def test_infer_json_basic_lib(basic_stream_ndjson):
    firstline = get_firstline(basic_stream_ndjson)
    sql = generate_ddl(firstline, table_name="foo1", primary_key="id")
    computed = sql_canonicalize(sql)
    assert get_basic_sql_reference(table_name="foo1") == computed


def test_infer_json_basic_cli_file(basic_stream_ndjson):
    runner = CliRunner()
    result = runner.invoke(cli, "infer-ddl --dialect=crate --table-name=foo2 tests/basic.ndjson")
    assert result.exit_code == 0

    computed = sql_canonicalize(result.stdout)
    assert get_basic_sql_reference(table_name="foo2") == computed
