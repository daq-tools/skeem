import dataclasses
import logging
import typing as t
from pathlib import Path

from eskema.type import ContentType
from eskema.util import sql_canonicalize, sql_pretty

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Resource:
    data: t.Any
    path: t.Optional[t.Union[Path, str]] = None
    content_type: t.Optional[t.Union[ContentType, str]] = None
    type: t.Optional[ContentType] = None  # noqa: A003

    def configure(self):

        # Default values.
        self.path = Path(self.path) if self.path else None

        # Croak if content type can not be derived.
        if not self.path and not self.content_type:
            raise NotImplementedError(
                "Introspection-based content type detection not implemented yet. "
                "Please specify input filename, `content_type` parameter, or `--content-type` option."
            )

        # Derive content type from file extension or mimetype / short name.
        if self.path:
            self.type = ContentType.from_filename(self.path)
            logger.info(f"Detected {self.type} from filename")
        if self.content_type:
            self.type = ContentType.from_name(self.content_type)
            logger.info(f"Using {self.type} as specified")


@dataclasses.dataclass
class SqlTarget:
    dialect: t.Optional[str] = None
    table_name: t.Optional[str] = None
    primary_key: t.Optional[str] = None


@dataclasses.dataclass
class SqlResult:
    sql: str

    @property
    def canonical(self):
        return sql_canonicalize(self.sql)

    @property
    def pretty(self):
        return sql_pretty(self.sql)
