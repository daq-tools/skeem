from io import BytesIO, StringIO
from pathlib import Path

import pytest
import sqlalchemy as sa


@pytest.fixture
def ndjson_file_basic():
    return Path("tests/testdata/basic.ndjson")


@pytest.fixture
def ndjson_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.ndjson"


@pytest.fixture
def ndjson_github_url_basic():
    return "github://daq-tools:eskema@/tests/testdata/basic.ndjson"


@pytest.fixture
def csv_file_basic():
    return Path("tests/testdata/basic.csv")


@pytest.fixture
def csv_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.csv"


@pytest.fixture
def json_records_file_basic():
    return Path("tests/testdata/basic-records.json")


@pytest.fixture
def json_records_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic-records.json"


@pytest.fixture
def json_document_file_basic():
    return Path("tests/testdata/basic-document.json")


@pytest.fixture
def json_document_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic-document.json"


@pytest.fixture
def json_nested_file_basic():
    return Path("tests/testdata/basic-nested.json")


@pytest.fixture
def json_nested_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic-nested.json"


@pytest.fixture
def line_protocol_file_basic():
    return Path("tests/testdata/basic.lp")


@pytest.fixture
def line_protocol_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.lp"


@pytest.fixture
def line_protocol_file_irregular():
    return Path("tests/testdata/air-sensor-data-irregular.lp")


@pytest.fixture
def xlsx_file_basic():
    return Path("tests/testdata/basic.xlsx")


@pytest.fixture
def xlsx_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.xlsx"


@pytest.fixture
def ods_file_basic():
    return Path("tests/testdata/basic.ods")


@pytest.fixture
def ods_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.ods"


@pytest.fixture
def parquet_file_basic():
    return Path("tests/testdata/basic.parquet")


@pytest.fixture
def parquet_url_basic():
    return "https://raw.githubusercontent.com/daq-tools/eskema/main/tests/testdata/basic.parquet"


@pytest.fixture
def ndjson_stream_basic():
    """
    A stream of input data. Here, in NDJSON (ex. LDJSON) format, aka. JSON Lines.

    http://ndjson.org/
    """
    return StringIO(
        """
{"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
{"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
    """.strip()
    )


@pytest.fixture
def parquet_stream_basic(parquet_file_basic):
    """
    A stream of input data. Here, in Parquet format.

    https://en.wikipedia.org/wiki/Apache_Parquet
    """
    return BytesIO(open(parquet_file_basic, "rb").read())


class SqlAlchemyTableExtendExisting(sa.Table):
    """
    The test cases re-use the same table names within different test cases.
    Without using `extend_existing = True`, SQLAlchemy would croak on that, like:

        InvalidRequestError("Table 'basic' is already defined for this MetaData instance.
                             Specify 'extend_existing=True' to redefine options and columns
                             on an existing Table object.")
    """

    def __new__(cls, *args, **kw):
        kw["extend_existing"] = True
        return super().__new__(cls, *args, **kw)


sa.Table = SqlAlchemyTableExtendExisting
