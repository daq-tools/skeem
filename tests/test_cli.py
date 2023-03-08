import pytest
from click.testing import CliRunner

from skeem.cli import cli


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
