import pytest
from click.testing import CliRunner

from eskema.cli import cli
from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlTarget


def test_generic_infer_library_without_dialect():
    """
    It is needed to specify an SQL dialect.
    """
    with pytest.raises(ValueError) as ex:
        sg = SchemaGenerator(
            resource=Resource(
                data=None,
                content_type=None,
            ),
            target=SqlTarget(
                table_name="foo1",
                primary_key="id",
            ),
        )
        sg.to_sql_ddl()
    assert ex.match("Inferring the database schema needs an SQLAlchemy dialect")


def test_generic_infer_library_without_content_type():
    """
    It is needed to specify a content type.
    """
    with pytest.raises(NotImplementedError) as ex:
        sg = SchemaGenerator(Resource(data=None), SqlTarget(dialect="crate", table_name="foo1", primary_key="id"))
        sg.to_sql_ddl()
    assert ex.match("Introspection-based content type detection not implemented yet")


def test_generic_infer_library_unknown_content_type():
    """
    It is needed to specify a valid content type.
    """
    with pytest.raises(ValueError) as ex:
        sg = SchemaGenerator(
            Resource(data=None, content_type="unknown"),
            SqlTarget(dialect="crate", table_name="foo1", primary_key="id"),
        )
        sg.to_sql_ddl()
    assert ex.match("'unknown' is not a valid ContentType or ContentTypeMime")


def test_generic_infer_cli_stdin_without_content_type():
    """
    CLI test: Reading data from stdin needs a content type.
    """
    runner = CliRunner()

    with pytest.raises(NotImplementedError) as ex:
        runner.invoke(
            cli,
            args="infer-ddl --dialect=crate --table-name=foo -",
            input="",
            catch_exceptions=False,
        )
    assert ex.match("Introspection-based content type detection not implemented yet.")
