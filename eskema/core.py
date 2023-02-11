import logging
import typing as t
import warnings

from eskema.autopk import infer_pk
from eskema.model import Resource, SqlResult, SqlTarget
from eskema.sources import SourcePlus
from eskema.type import ContentType

logger = logging.getLogger(__name__)


class SchemaGenerator:
    """
    Generate SQL DDL schema from input data.
    """

    def __init__(
        self,
        resource: Resource,
        target: SqlTarget,
        backend: t.Optional[str] = "ddlgen",
    ):
        self.resource = resource
        self.target = target
        self.backend = backend
        self.configure()

    def configure(self):
        """
        Apply default configuration.

        - Run sanity checks.
        - Derive table name from file name.
        - Peek input resource and derive content type.
        """
        # Sanity checks.
        if not self.target.dialect:
            raise ValueError("Inferring the database schema needs an SQLAlchemy dialect")

        # Derive table name from input file name or data.
        if not self.target.table_name and self.resource.path:
            self.target.table_name = self.resource.path.stem

        self.resource.peek()

    def to_sql_ddl(self) -> SqlResult:
        """
        Infer field/column schema from input data and generate SQL DDL statement.
        """
        if self.backend == "ddlgen":
            return self._ddl_ddlgen()
        elif self.backend == "frictionless" or self.backend == "fl":
            return self._ddl_frictionless()
        else:
            raise NotImplementedError(f"Backend '{self.backend}' not implemented")

    def _ddl_frictionless(self) -> SqlResult:

        # Suppress warnings of BeautifulSoup
        from bs4 import GuessedAtParserWarning

        warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

        import frictionless.formats
        import sqlalchemy as sa
        from ddlgenerator.ddlgenerator import _dump

        from eskema.ddlgen.ddlgenerator import TablePlus

        # Sanity checks.
        if self.resource.type is None:
            raise ValueError("Unable to infer schema without resource type")

        # When primary key is not given, try to infer it from the data.
        # TODO: Make `infer_pk` obtain a `Resource` instance, and/or refactor as method.
        if self.target.primary_key is None:

            resource = frictionless.Resource(self.resource.path)
            df = resource.to_pandas()

            self.target.primary_key = infer_pk(df, self.resource.type, address=self.resource.address)

        # Infer schema.
        engine = sa.create_mock_engine(f"{self.target.dialect}://", executor=_dump)
        mapper = frictionless.formats.sql.SqlMapper(engine)
        schema = frictionless.Schema.describe(self.resource.path)

        # Amend schema with primary key information.
        pk_field = schema.get_field(self.target.primary_key)
        pk_field.required = True
        schema.primary_key = [self.target.primary_key]

        # Create SQLAlchemy table from schema.
        table = mapper.write_schema(schema, table_name=self.target.table_name, with_metadata=False)

        # Serialize SQLAlchemy table instance to SQL DDL, using `ddlgenerator`.
        tt = TablePlus(data="")
        tt.table = table
        sql = tt.ddl(dialect=self.target.dialect, creates=True, drops=False)
        return SqlResult(sql)

    def _ddl_ddlgen(self) -> SqlResult:

        from eskema.ddlgen.ddlgenerator import TablePlus

        # Sanity checks.
        if self.resource.type is None:
            raise ValueError("Unable to infer schema without resource type")

        # Only peek at the first bytes of data.
        indata = self.resource.read_data()

        # When primary key is not given, try to infer it from the data.
        # TODO: Make `infer_pk` obtain a `Resource` instance, and/or refactor as method.
        if self.target.primary_key is None:
            self.target.primary_key = infer_pk(indata, self.resource.type, address=self.resource.address)

        # Wrap data into data-dispenser's `Source` instance.
        suffix = ContentType.to_suffix(self.resource.type)
        data = SourcePlus(indata, ext=suffix, table=self.resource.address)

        # Infer schema from data.
        table = TablePlus(
            data=data,
            table_name=self.target.table_name,
            varying_length_text=True,
            uniques=False,
            pk_name=self.target.primary_key,
            force_pk=False,
            reorder=False,
            loglevel=logging.DEBUG,
            limit=None,
        )

        # Convert schema to SQL DDL statement.
        sql = table.sql(dialect=self.target.dialect, creates=True, drops=False, inserts=False)
        return SqlResult(sql)
