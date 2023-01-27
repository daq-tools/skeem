import io
import textwrap

import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import PEEK_BYTES, SchemaGenerator
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.monkey import clean_key_name
from eskema.util import get_firstline, sql_canonicalize


def get_basic_sql_reference(table_name, primary_key="id"):
    """
    The reference how the inferred SQL should look like.
    """
    basic_reference = sql_canonicalize(
        textwrap.dedent(
            f"""
        CREATE TABLE "{clean_key_name(table_name)}" (
            "id" INT NOT NULL,
            "name" STRING NOT NULL,
            "date" TIMESTAMP NOT NULL,
            "fruits" STRING NOT NULL,
            "price" DOUBLE NOT NULL,
            PRIMARY KEY ("{primary_key}")
        );
    """
        )
    )
    return basic_reference.strip("\n")


@pytest.fixture
def basic_stream_ndjson():
    """
    A stream of input data. Here, in ndjson format, aka. jsonl.

    http://ndjson.org/
    """
    return io.StringIO(
        """
{"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
{"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
    """.lstrip()
    )


def test_ndjson_infer_library_success(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    firstline = get_firstline(basic_stream_ndjson)
    sg = SchemaGenerator(
        resource=Resource(
            data=firstline,
            content_type="ndjson",
        ),
        target=SqlTarget(
            dialect="crate",
            table_name="foo1",
            primary_key="id",
        ),
    )

    computed = sg.to_sql_ddl().canonical
    reference = get_basic_sql_reference(table_name="foo1")
    assert computed == reference


def test_ndjson_infer_library_without_dialect(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    firstline = get_firstline(basic_stream_ndjson)
    with pytest.raises(ValueError) as ex:
        sg = SchemaGenerator(
            resource=Resource(
                data=firstline,
                content_type="ndjson",
            ),
            target=SqlTarget(
                table_name="foo1",
                primary_key="id",
            ),
        )
        sg.to_sql_ddl()
    assert ex.match("Inferring the database schema needs an SQLAlchemy dialect")


def test_ndjson_infer_library_without_content_type(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    firstline = get_firstline(basic_stream_ndjson)
    with pytest.raises(NotImplementedError) as ex:
        sg = SchemaGenerator(Resource(data=firstline), SqlTarget(dialect="crate", table_name="foo1", primary_key="id"))
        sg.to_sql_ddl()
    assert ex.match("Introspection-based content type detection not implemented yet")


def test_ndjson_infer_library_unknown_content_type(basic_stream_ndjson):
    """
    Verify basic library use.
    """
    firstline = get_firstline(basic_stream_ndjson)
    with pytest.raises(ValueError) as ex:
        sg = SchemaGenerator(
            Resource(data=firstline, content_type="unknown"),
            SqlTarget(dialect="crate", table_name="foo1", primary_key="id"),
        )
        sg.to_sql_ddl()
    assert ex.match("'unknown' is not a valid ContentType or ContentTypeShort")


def test_ndjson_infer_cli_file_without_tablename(ndjson_file_basic):
    """
    CLI test: Table name is correctly derived from the input file name or data.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate {ndjson_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="basic")
    assert computed == reference


def test_ndjson_infer_cli_file_with_tablename(ndjson_file_basic):
    """
    CLI test: Table name takes precedence when obtained from the user.
    """
    runner = CliRunner()
    result = runner.invoke(cli, f"infer-ddl --dialect=crate --table-name=foo2 {ndjson_file_basic}")
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name="foo2")
    assert computed == reference


@pytest.mark.parametrize("content_type", ["ndjson", "jsonl", "application/x-ldjson"])
def test_ndjson_infer_cli_stdin_with_content_type(basic_stream_ndjson, content_type: str):
    """
    CLI test: Read data from stdin.
    """
    runner = CliRunner()
    table_name = f"foo3_{content_type}"
    result = runner.invoke(
        cli,
        args=f"infer-ddl --dialect=crate --table-name={table_name} --content-type={content_type} -",
        input=basic_stream_ndjson.read(PEEK_BYTES),
    )
    assert result.exit_code == 0

    computed = SqlResult(result.stdout).canonical
    reference = get_basic_sql_reference(table_name=table_name)
    assert computed == reference


def test_ndjson_infer_cli_stdin_without_content_type(basic_stream_ndjson):
    """
    CLI test: Read data from stdin.
    """
    runner = CliRunner()

    with pytest.raises(NotImplementedError) as ex:
        runner.invoke(
            cli,
            args="infer-ddl --dialect=crate --table-name=foo -",
            input=basic_stream_ndjson.read(PEEK_BYTES),
            catch_exceptions=False,
        )
    assert ex.match("Introspection-based content type detection not implemented yet.")
