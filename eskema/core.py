import logging

from eskema.autopk import infer_pk
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.util import get_firstline

PEEK_BYTES = 10000

logger = logging.getLogger(__name__)


class SchemaGenerator:
    """
    Generate SQL DDL schema from input data.
    """

    def __init__(
        self,
        resource: Resource,
        target: SqlTarget,
    ):
        self.resource = resource
        self.target = target
        self.configure()

    def configure(self):
        # Sanity checks.
        if not self.target.dialect:
            raise ValueError("Inferring the database schema needs an SQLAlchemy dialect")

        # Derive table name from input file name or data.
        if not self.target.table_name and self.resource.path:
            self.target.table_name = self.resource.path.stem

        self.resource.configure()

    def to_sql_ddl(self) -> SqlResult:
        from ddlgenerator.ddlgenerator import Table

        # Only peek at the first bytes of data.
        indata = self.resource.data.read(PEEK_BYTES)

        # When primary key is not given, try to infer it from the data.
        if self.target.primary_key is None:
            self.target.primary_key = infer_pk(indata)

        firstline = get_firstline(indata)
        table = Table(
            firstline,
            table_name=self.target.table_name,
            varying_length_text=True,
            uniques=False,
            pk_name=self.target.primary_key,
            force_pk=True,
            reorder=False,
            loglevel=logging.DEBUG,
            limit=None,
        )
        sql = table.sql(dialect=self.target.dialect, creates=True, drops=False, inserts=False)
        return SqlResult(sql)
