from pathlib import Path

import pytest
import sqlalchemy as sa


@pytest.fixture
def ndjson_file_basic():
    return Path("tests/testdata/basic.ndjson")


@pytest.fixture
def csv_file_basic():
    return Path("tests/testdata/basic.csv")


@pytest.fixture
def json_records_file_basic():
    return Path("tests/testdata/basic-records.json")


@pytest.fixture
def json_document_file_basic():
    return Path("tests/testdata/basic-document.json")


@pytest.fixture
def xlsx_file_basic():
    return Path("tests/testdata/basic.xlsx")


@pytest.fixture
def ods_file_basic():
    return Path("tests/testdata/basic.ods")


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
