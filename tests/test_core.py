import io

import pandas as pd
import pytest

from skeem.autopk import infer_pk
from skeem.core import SchemaGenerator
from skeem.model import Resource, SqlTarget


def test_schema_generator_without_dialect():
    """
    It is needed to specify an SQL dialect.
    """
    with pytest.raises(ValueError) as ex:
        SchemaGenerator(
            resource=Resource(data=None),
            target=SqlTarget(),
        )
    assert ex.match("Inferring the database schema needs an SQLAlchemy dialect")


def test_schema_generator_without_content_type():
    """
    It is needed to specify a content type.
    """
    with pytest.raises(NotImplementedError) as ex:
        sg = SchemaGenerator(
            resource=Resource(data=None),
            target=SqlTarget(dialect="postgresql"),
        )
        sg.to_sql_ddl()
    assert ex.match("Introspection-based content type detection not implemented yet")


def test_schema_generator_invalid_content_type():
    """
    It is needed to specify a valid content type.
    """
    with pytest.raises(ValueError) as ex:
        sg = SchemaGenerator(
            resource=Resource(data=None, content_type="unknown"),
            target=SqlTarget(dialect="postgresql"),
        )
        sg.to_sql_ddl()
    assert ex.match("'unknown' is not a valid ContentType or ContentTypeMime")


@pytest.mark.xfail
def test_schema_generator_without_resource_type():
    # Let's create a _valid_ `SchemaGenerator` instance first.
    sg = SchemaGenerator(
        resource=Resource(data=io.StringIO("a,b"), content_type="csv"),
        target=SqlTarget(dialect="postgresql"),
    )

    # Let's invalidate the resource type on purpose.
    sg.resource.type = None

    # Proof that `to_sql_ddl()` sanity checks are working.
    with pytest.raises(ValueError) as ex:
        sg.to_sql_ddl()
    assert ex.match("Unable to infer schema without resource type")


def test_infer_pk_from_dataframe():
    """
    Infer primary key from pandas DataFrame.
    """
    data = [
        {"id": 1, "name": "foo", "date": pd.Timestamp("2014-10-31 09:22:56"), "fruits": "apple,banana", "price": 0.42},
        {"id": 2, "name": "bar", "date": pd.NaT, "fruits": "pear", "price": 0.84},
    ]
    df = pd.DataFrame.from_dict(data=data)
    pk = infer_pk(df)
    assert pk == "id"
