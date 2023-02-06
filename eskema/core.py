import logging

from eskema.autopk import infer_pk
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.sources import SourcePlus
from eskema.type import ContentType
from eskema.util import get_firstline

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

        if self.resource.type is None:
            raise ValueError("Unable to infer schema without resource type")

        # Only peek at the first bytes of data.
        indata = self.resource.read_data()

        # When inferring from NDJSON, use only the first line.
        if ContentType.is_ndjson(self.resource.type):
            indata = get_firstline(indata, nrows=1)

        # When primary key is not given, try to infer it from the data.
        if self.target.primary_key is None:
            self.target.primary_key = infer_pk(indata, self.resource.type)
            indata.seek(0)

        if self.resource.type is ContentType.CSV:
            indata = get_firstline(indata, nrows=2)

        # TODO: Still needed?
        data = indata

        suffix = ContentType.to_suffix(self.resource.type)
        table = Table(
            data=SourcePlus(data, ext=suffix),
            table_name=self.target.table_name,
            varying_length_text=True,
            uniques=False,
            pk_name=self.target.primary_key,
            force_pk=False,
            reorder=False,
            loglevel=logging.DEBUG,
            limit=None,
        )
        sql = table.sql(dialect=self.target.dialect, creates=True, drops=False, inserts=False)
        return SqlResult(sql)
