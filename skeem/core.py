import logging
import typing as t
import warnings
from pathlib import Path

import pandas as pd

from skeem.autopk import infer_pk
from skeem.exception import UnknownContentType
from skeem.model import Resource, SqlResult, SqlTarget
from skeem.settings import FRICTIONLESS_CONTENT_TYPES
from skeem.type import ContentType
from skeem.util.data import to_bytes

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
            self.target.table_name = Path(self.resource.path).stem

    def to_sql_ddl(self) -> SqlResult:
        """
        Infer field/column schema from input data and generate SQL DDL statement.
        """

        logger.info(f"Selected backend: {self.backend}")
        fallback = False
        try:
            self.resource.detect_type()
        except UnknownContentType:
            logger.info("WARNING: Unable to detect content type")
            fallback = True

        choose_frictionless = (
            fallback or self.backend in ["frictionless", "fl"] or self.resource.type in FRICTIONLESS_CONTENT_TYPES
        )
        if choose_frictionless:
            self.backend = "frictionless"
        logger.info(f"Effective backend: {self.backend}")

        if self.backend == "ddlgen":
            return self._ddl_ddlgen()
        elif self.backend == "frictionless":
            return self._ddl_frictionless()
        else:
            raise NotImplementedError(f"Backend '{self.backend}' not implemented")

    def _ddl_frictionless(self) -> SqlResult:
        # Suppress warnings of BeautifulSoup
        from bs4 import GuessedAtParserWarning

        warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

        from frictionless import Control, Schema
        from frictionless.formats import ExcelControl, OdsControl, SqlMapper

        from skeem.ddlgen.ddlgenerator import TablePlus
        from skeem.frictionless.resource import TableSampleResource

        # Sanity checks.
        if not self.target.dialect:
            raise ValueError("Inferring the database schema needs an SQLAlchemy dialect")

        frictionless_args: t.Dict[str, t.Union[str, t.IO]] = {}
        if self.resource.path is not None:
            frictionless_args["path"] = str(self.resource.path)
        elif self.resource.data is not None:
            # Sanity checks.
            if self.resource.type is None:
                raise ValueError("Unable to infer schema without resource type")
            frictionless_args["format"] = self.resource.type.suffix.lstrip(".")

            payload = self.resource.data.read()
            data = to_bytes(payload)
            frictionless_args["data"] = data
        else:
            raise ValueError("Unable to read any data")

        # Define resource controls.
        control: t.Union[Control, None] = None
        if self.resource.type is ContentType.ODS:
            control = OdsControl(sheet=self.resource.address or 1)
        elif self.resource.type is ContentType.XLSX:
            control = ExcelControl(sheet=self.resource.address or 1)

        # Open resource.
        logger.info(f"Opening resource {frictionless_args}. type={self.resource.type}, control={control}")
        resource = TableSampleResource(**frictionless_args, control=control)  # type: ignore[arg-type]

        # When primary key is not given, try to infer it from the data.
        # TODO: Make `infer_pk` obtain a `Resource` instance, and/or refactor as method.
        # TODO: Optimize runtime by not needing to open the resource twice.
        if self.target.primary_key is None:
            logger.info("Converging resource to pandas DataFrame")
            df: pd.DataFrame = resource.to_pandas()
            logger.info(f"pandas DataFrame size={len(df)}")

            logger.info("Inferring primary key")
            self.target.primary_key = infer_pk(df, self.resource.type, address=self.resource.address)

        # Infer schema.
        logger.info("Inferring schema")
        mapper = SqlMapper(dialect=self.target.dialect)
        descriptor = resource.to_descriptor()

        # Either `schema` is already present, or it needs to be established by invoking `describe` first.
        if "schema" in descriptor:
            schema = Schema.from_descriptor(descriptor["schema"])
        else:
            schema = Schema.describe(**frictionless_args, control=control)

        logger.debug(f"Inferred schema: {schema}")

        # Amend schema with primary key information.
        if self.target.primary_key is not None:
            pk_field = schema.get_field(self.target.primary_key)
            pk_field.required = True
            schema.primary_key = [self.target.primary_key]

        # Sanity checks.
        if not self.target.table_name:
            raise ValueError("Table name must not be empty")

        # Create SQLAlchemy table from schema.
        logger.info("Converging schema to SQLAlchemy")
        table = mapper.write_schema(schema, table_name=self.target.table_name, with_metadata=False)

        # Serialize SQLAlchemy table instance to SQL DDL, using `ddlgenerator`.
        logger.info("Serialize SQLAlchemy schema to SQL DDL statement")
        tt = TablePlus(data="")
        tt.table = table
        sql = tt.ddl(dialect=self.target.dialect, creates=True, drops=False)
        return SqlResult(sql)

    def _ddl_ddlgen(self) -> SqlResult:
        from skeem.ddlgen.ddlgenerator import TablePlus
        from skeem.ddlgen.sources import SourcePlus

        # Sanity checks.
        if self.resource.type is None:
            raise ValueError("Unable to infer schema without resource type")

        if self.resource.type is ContentType.GZIP and self.resource.content_type is None:
            raise ValueError("Resource content type is required when resource container type is Gzip")

        # Only peek at the first bytes of data.
        logger.info(f"Opening resource {self.resource}")
        indata = self.resource.peek()

        # When primary key is not given, try to infer it from the data.
        # TODO: Make `infer_pk` obtain a `Resource` instance, and/or refactor as method.
        if self.target.primary_key is None:
            self.target.primary_key = infer_pk(indata, self.resource.type, address=self.resource.address)

        # Wrap data into data-dispenser's `Source` instance.
        logger.info("Converging resource to ddlgen source object")
        data = SourcePlus(indata, ext=self.resource.type.suffix, table=self.resource.address)

        # Infer schema from data.
        logger.info("Inferring schema")
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
