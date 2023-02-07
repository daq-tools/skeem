"""
Example program to infer an SQL DDL statement from NDJSON input data.

The NDJSON (ex. LDJSON) format, aka. JSON Lines, is a Newline Delimited JSON
format, suitable for processing JSON data in a streaming manner.

- http://ndjson.org/
- https://en.wikipedia.org/wiki/JSON_streaming
- https://github.com/ndjson/ndjson.github.io/issues/1#issuecomment-109935996
"""
import io
import typing as t

from eskema.core import SchemaGenerator
from eskema.model import Resource, SqlTarget


def get_data() -> t.IO:
    """
    Provide sample NDJSON data.
    """
    return io.StringIO(
        """
        {"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
        {"id":2,"name":"bar","date":null,"fruits":"pear","price":0.84}
        """
    )


def infer_ddl_schema():
    sg = SchemaGenerator(
        resource=Resource(data=get_data(), content_type="ndjson"),
        target=SqlTarget(dialect="crate", table_name="testdrive"),
    )
    return sg.to_sql_ddl().pretty


if __name__ == "__main__":
    print(infer_ddl_schema())  # noqa: T201
