import io

import pandas as pd
import pandas._testing as tm
import pytest

from eskema.io import to_dataframe
from eskema.type import ContentType


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
