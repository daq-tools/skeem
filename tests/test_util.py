import io
import json
import logging
import re
from contextlib import redirect_stdout
from unittest import mock

import pytest

from skeem.io import json_get_first_records
from skeem.util.cli import boot_click
from skeem.util.data import get_firstline, head, jd
from skeem.util.sql import sql_pretty


def test_jd():
    data = {"foo": "bar"}

    # Use `jd` function while capturing stdout.
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        jd(data)

    # Verify result.
    buffer.seek(0)
    result = json.load(buffer)
    assert result == data


def test_sql_pretty():
    sql_unformatted = """
SELECT *
\tFROM table WHERE x="y";
    """.strip()
    assert sql_pretty(sql_unformatted, reindent=True) == 'SELECT *\nFROM TABLE\nWHERE x="y";'


def test_boot_click_loglevel_default():
    with mock.patch("skeem.util.cli.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=False, debug=False)
    setup_logging_mock.assert_called_once_with(level=logging.WARNING)


def test_boot_click_loglevel_verbose():
    with mock.patch("skeem.util.cli.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=True, debug=False)
    setup_logging_mock.assert_called_once_with(level=logging.INFO)


def test_boot_click_loglevel_debug():
    with mock.patch("skeem.util.cli.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=False, debug=True)
    setup_logging_mock.assert_called_once_with(level=logging.DEBUG)


def test_get_firstline_string():
    indata = "first\nsecond"
    firstline = get_firstline(indata).read()
    assert firstline == "first"


def test_get_firstline_textwrapper():
    indata = io.TextIOWrapper(io.BytesIO(b"first\nsecond"))
    firstline = get_firstline(indata).read()
    assert firstline == "first\n"


def test_get_firstline_path(tmp_path):
    indata = tmp_path.joinpath("testfile")
    indata.write_text("first\nsecond")
    firstline = get_firstline(indata).read()
    assert firstline == "first\n"


def test_get_firstline_unknown_type():
    with pytest.raises(TypeError) as ex:
        get_firstline(42.42).read()
    assert ex.match(re.escape("Unable to decode first 1 line(s) from data. type=float"))


def test_json_get_first_records_empty():
    with pytest.raises(ValueError) as ex:
        json_get_first_records(io.StringIO(""))
    assert ex.match("Unable to parse JSON document in streaming mode. Reason: Document is empty")


def test_json_get_first_records_invalid():
    with pytest.raises(ValueError) as ex:
        json_get_first_records(io.StringIO("foobar"))
    assert ex.match("Unable to parse JSON document in streaming mode. Reason: Invalid JSON character: 'o' at index 1")


def test_json_get_first_records_success():
    records = json_get_first_records(io.StringIO('[{"foo":"bar"}]'))
    assert dict(records[0]) == {"foo": "bar"}


def test_head_full():
    gen = head(io.StringIO("foo\nbar\nbaz"))
    assert next(gen) == "foo\n"
    assert next(gen) == "bar\n"
    assert next(gen) == "baz"
    with pytest.raises(StopIteration):
        next(gen)


def test_head_bytes():
    gen = head(io.StringIO("foo\nbar\nbaz"), c=2)
    assert next(gen) == "fo"
    with pytest.raises(StopIteration):
        next(gen)


def test_head_lines():
    gen = head(io.StringIO("foo\nbar\nbaz"), n=2)
    assert next(gen) == "foo\n"
    assert next(gen) == "bar\n"
    with pytest.raises(StopIteration):
        next(gen)
