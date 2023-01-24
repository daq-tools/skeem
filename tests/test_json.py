import io

from eskema.core import generate_ddl
from eskema.util import canonicalize_sql


def test_infer_json_basic():
    firstline = io.StringIO(
        """
    {"id":1,"name":"foo","date":"2014-10-31 09:22:56","fruits":"apple,banana","price":0.42}
    """
    )
    sql = generate_ddl(firstline, "foo", primary_key="id")
    computed = canonicalize_sql(sql)
    reference = canonicalize_sql(
        """
CREATE TABLE "foo" (
    "id" INT NOT NULL,
    "name" STRING NOT NULL,
    "date" TIMESTAMP NOT NULL,
    "fruits" STRING NOT NULL,
    "price" DOUBLE NOT NULL,
    PRIMARY KEY ("id")
);
"""
    )

    assert computed == reference
