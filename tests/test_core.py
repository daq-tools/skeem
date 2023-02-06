import io

import pytest

from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlTarget


def test_schema_generator_without_dialect():
    with pytest.raises(ValueError) as ex:
        SchemaGenerator(
            resource=Resource(data=None),
            target=SqlTarget(),
        )
    assert ex.match("Inferring the database schema needs an SQLAlchemy dialect")


def test_schema_generator_without_content_type():
    with pytest.raises(NotImplementedError) as ex:
        SchemaGenerator(
            resource=Resource(data=None),
            target=SqlTarget(dialect="postgresql"),
        )
    assert ex.match("Introspection-based content type detection not implemented yet")


def test_schema_generator_invalid_content_type():
    with pytest.raises(ValueError) as ex:
        SchemaGenerator(
            resource=Resource(data="", content_type="foo"),
            target=SqlTarget(dialect="postgresql"),
        )
    assert ex.match("'foo' is not a valid ContentType or ContentTypeShort")


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
