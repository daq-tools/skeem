import dataclasses
import io
import logging
import typing as t
from pathlib import Path

import fsspec

from eskema.settings import PEEK_LINES
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

    def peek(self):
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

    def read_data(self) -> t.IO:
        """
        Only peek at the first bytes of data.

        TODO: Refactor to `loader` module?
        """
        binary_files = [ContentType.XLSX, ContentType.ODS]

        if self.data is None and self.path is not None:
            self.data = fsspec.open(self.path, mode="rb").open()

        # Sanity checks
        if self.data is None:
            raise ValueError("Unable to open resource")

        # Only optionally seek to the file's beginning.
        if hasattr(self.data, "seekable") and self.data.seekable():
            self.data.seek(0)

        if self.type in binary_files:
            return io.BytesIO(self.data.read())
        else:
            if self.type is ContentType.JSON:
                logger.info("WARNING: Hitting a speed bump by needing to read JSON document as a whole")
                payload = self.data.read()
            else:
                empty = ""
                if isinstance(self.data, io.BytesIO) or (hasattr(self.data, "mode") and "b" in self.data.mode):
                    empty = b""  # type: ignore[assignment]
                payload = empty.join(self.data.readlines(PEEK_LINES))  # type: ignore[arg-type]
            if isinstance(payload, str):
                payload = payload.encode()
            return io.BytesIO(payload)


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
