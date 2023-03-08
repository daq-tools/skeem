import io

import pandas as pd
import pandas._testing as tm
import pytest

from skeem.io import peek, to_dataframe
from skeem.type import ContentType


def test_peek_success():
    assert peek(data="foo").read() == b"foo"


def test_peek_empty():
    assert peek(data="").read() == b""


def test_peek_none():
    with pytest.raises(TypeError) as ex:
        peek(data=None)
    assert ex.match("No method for peeking at data, type=NoneType")


def test_peek_int():
    with pytest.raises(TypeError) as ex:
        peek(data=42)
    assert ex.match("No method for peeking at data, type=int")


def test_peek_stream_full(basic_stream_csv):
    """
    Peeking without limits is equivalent to reading the whole file.
    """
    assert (
        peek(data=basic_stream_csv).read()
        == b'id,name,date,fruits,price\n1,"foo","2014-10-31T09:22:56","apple,banana",0.42\n2,"bar",,"pear",0.84'
    )


def test_peek_stream_partial(basic_stream_csv):
    """
    Peeking into the head of a stream with a certain amount of bytes still honors the concept of lines.
    """
    assert (
        peek(data=basic_stream_csv, peek_bytes=60).read()
        == b'id,name,date,fruits,price\n1,"foo","2014-10-31T09:22:56","apple,banana",0.42\n'
    )


def test_to_dataframe_csv(csv_file_basic):
    data = io.BytesIO(csv_file_basic.read_bytes())
    records = [
        {"id": 1, "name": "foo", "date": "2014-10-31T09:22:56", "fruits": "apple,banana", "price": 0.42},
        {"id": 2, "name": "bar", "date": None, "fruits": "pear", "price": 0.84},
    ]

    df_reference = pd.DataFrame.from_records(records)
    df_computed = to_dataframe(data=data, content_type=ContentType.CSV)
    tm.assert_frame_equal(df_reference, df_computed)


def test_to_dataframe_empty_data():
    with pytest.raises(ValueError) as ex:
        to_dataframe(data=None, content_type=None)
    assert ex.match("Unable to operate on empty data")


def test_to_dataframe_no_content_type():
    with pytest.raises(TypeError) as ex:
        to_dataframe(data=io.BytesIO(), content_type=None)
    assert ex.match(
        r"Failed to infer primary key with invalid content type "
        r"\(value=None, type=NoneType\), expected `ContentType`"
    )


def test_to_dataframe_csv_empty():
    with pytest.raises(ValueError) as ex:
        to_dataframe(data=io.BytesIO(), content_type=ContentType.CSV)
    assert ex.match("No columns to parse from file")


def test_to_dataframe_grib2():
    with pytest.raises(ValueError) as ex:
        to_dataframe(data=io.BytesIO(), content_type=ContentType.GRIB2)
    assert ex.match("Unable to process content type: ContentType.GRIB2")
