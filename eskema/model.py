import dataclasses
import logging
import typing as t
from pathlib import Path

import fsspec

from eskema.io import peek
from eskema.settings import PEEK_BYTES, PEEK_LINES
from eskema.type import ContentType
from eskema.util import sql_canonicalize, sql_pretty

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Resource:
    """
    A wrapper around input data.
    """

    data: t.Optional[t.Union[t.IO[t.Any], None]] = None
    address: t.Optional[str] = None
    path: t.Optional[t.Union[Path, str]] = None
    content_type: t.Optional[t.Union[ContentType, str]] = None
    type: t.Optional[ContentType] = None  # noqa: A003

    def detect_type(self):
        """
        Introspect input data and derive content type.
        Currently, it only detects the content type from the filename extension.

        # TODO: Implement introspection-based content type detection.
        """

        # Default values.
        self.path = self.path or None

        # Croak if content type can not be derived.
        if not self.path and not self.content_type:
            raise NotImplementedError(
                "Introspection-based content type detection not implemented yet. "
                "Please specify input filename, `content_type` parameter, or `--content-type` option."
            )

        # Derive content type from file extension or mimetype / short name.
        if self.path:
            self.type = ContentType.from_filename(self.path)
            logger.info(f"Detected type from filename: {self.type}")
        if self.content_type:
            self.type = ContentType.from_name(self.content_type)
            logger.info(f"Using specified type: {self.type}")

    def peek(self) -> t.IO:
        """
        Only peek at the first bytes of data.
        """

        # Access a plethora of resources using `fsspec`.
        # TODO: Refactor to `eskema.io`.
        if self.data is None and self.path is not None:
            kwargs = {}
            if str(self.path).startswith("s3"):
                kwargs["anon"] = True
            self.data = fsspec.open(self.path, mode="rb", **kwargs).open()

        # Sanity checks
        if self.data is None:
            raise ValueError("Unable to open resource")

        # Peek into the first bytes/lines of data.
        return peek(data=self.data, content_type=self.type, peek_bytes=PEEK_BYTES, peek_lines=PEEK_LINES)


@dataclasses.dataclass
class SqlTarget:
    """
    Manage SQL target definition metadata.
    """

    dialect: t.Optional[str] = None
    table_name: t.Optional[str] = None
    primary_key: t.Optional[str] = None


@dataclasses.dataclass
class SqlResult:
    """
    Manage result SQL DDL statement.
    """

    sql: str

    @property
    def canonical(self) -> str:
        return sql_canonicalize(self.sql)

    @property
    def pretty(self) -> str:
        return sql_pretty(self.sql)
