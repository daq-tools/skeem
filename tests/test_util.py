import io
import json
import logging
from contextlib import redirect_stdout
from unittest import mock

import pytest

from eskema.util import boot_click, get_firstline, jd, sql_pretty


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
    with mock.patch("eskema.util.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=False, debug=False)
    setup_logging_mock.assert_called_once_with(level=logging.WARNING)


def test_boot_click_loglevel_verbose():
    with mock.patch("eskema.util.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=True, debug=False)
    setup_logging_mock.assert_called_once_with(level=logging.INFO)


def test_boot_click_loglevel_debug():
    with mock.patch("eskema.util.setup_logging") as setup_logging_mock:
        boot_click(None, verbose=False, debug=True)
    setup_logging_mock.assert_called_once_with(level=logging.DEBUG)


def test_get_firstline_string():
    indata = "first\nsecond"
    firstline = get_firstline(indata).read()
    assert firstline == "first"


def test_get_firstline_textwrapper():
    indata = io.TextIOWrapper(io.BytesIO(b"first\nsecond"))
    firstline = get_firstline(indata).read()
    assert firstline == "first"


def test_get_firstline_path(tmp_path):
    indata = tmp_path.joinpath("testfile")
    indata.write_text("first\nsecond")
    firstline = get_firstline(indata).read()
    assert firstline == "first"


def test_get_firstline_unknown_type():
    with pytest.raises(TypeError) as ex:
        get_firstline(42.42).read()
    assert ex.match("Unable to decode first line from data. type=float")
