import mimetypes
import typing as t
from enum import Enum
from pathlib import Path

from eskema.exception import UnknownContentType


def init():
    """
    Expand Python's MIME types map.

    Table comparing NDJSON (ex. LDJSON) and JSON Lines side-by-side:
    https://github.com/ndjson/ndjson.github.io/issues/1#issuecomment-109935996

    The listed MIME types are not officially registered, for some of them,
    there are a few hints, for others, the MIME type has been completely made up.

    - Parquet: https://issues.apache.org/jira/browse/PARQUET-1889?focusedCommentId=17468854#comment-17468854
    """
    mimetypes.init()
    mimetypes.types_map.update(
        {
            ".jsonl": "application/x-ndjson",
            ".ldjson": "application/x-ldjson",
            ".ldj": "application/x-ldjson",
            ".ndjson": "application/x-ndjson",
            ".parquet": "application/vnd.apache.parquet",
            ".parq": "application/vnd.apache.parquet",
            ".pq": "application/vnd.apache.parquet",
        }
    )


class ContentType(Enum):
    """
    Enumerate all supported content types and derive content type from input data.
    """

    # Primary definitions.
    CSV = "text/csv"
    JSON = "application/json"
    NDJSON = "application/x-ndjson"
    ODS = "application/vnd.oasis.opendocument.spreadsheet"
    PARQUET = "application/vnd.apache.parquet"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Secondary aliases.
    JSONL = "application/x-ndjson"
    LDJSON = "application/x-ldjson"

    @classmethod
    def from_filename(cls, filename: t.Union[Path, str]) -> "ContentType":
        """
        Derive content type from filename extension.

        >>> ContentType.from_filename("foo.csv")
        <ContentType.CSV: 'text/csv'>
        """
        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is None:
            raise UnknownContentType(f"Unable to guess content type from '{filename}'")
        return cls(mimetype)

    @classmethod
    def from_name(cls, name: str) -> "ContentType":
        """
        Derive content type from long and short name.

        >>> ContentType.from_name("csv")
        <ContentType.CSV: 'text/csv'>

        >>> ContentType.from_name("text/csv")
        <ContentType.CSV: 'text/csv'>
        """
        try:
            return ContentType(name)
        except ValueError:
            pass

        try:
            return ContentType(ContentTypeShort.resolve(name))
        except ValueError:
            pass

        raise ValueError(f"'{name}' is not a valid ContentType or ContentTypeShort")

    @classmethod
    def is_ndjson(cls, type_: "ContentType") -> bool:
        """
        Is content type any variant of NDJSON?
        """
        if type_ in [ContentType.NDJSON, ContentType.JSONL, ContentType.LDJSON]:
            return True
        else:
            return False

    @classmethod
    def to_suffix(cls, type_: "ContentType") -> str:
        """
        Derive filename extension from content type.
        """

        if type_ is ContentType.CSV:
            return ".csv"
        elif type_ is ContentType.JSON:
            return ".json"
        elif cls.is_ndjson(type_):
            return ".ndjson"
        elif type_ is ContentType.ODS:
            return ".ods"
        elif type_ is ContentType.PARQUET:
            return ".parquet"
        elif type_ is ContentType.XLSX:
            return ".xlsx"
        else:
            raise ValueError(f"Unable to compute suffix for content type '{type_}'")


class ContentTypeShort(Enum):
    """
    Manage short names of content types, mapping them to their corresponding mimetype counterparts.
    """

    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"
    LDJSON = "ldjson"
    NDJSON = "ndjson"
    ODS = "ods"
    PARQUET = "parquet"
    XLSX = "xlsx"

    @classmethod
    def resolve(cls, label: str) -> str:
        v1 = cls(label)
        mapping = {
            cls.CSV: ContentType.CSV.value,
            cls.JSON: ContentType.JSON.value,
            cls.JSONL: ContentType.NDJSON.value,
            cls.LDJSON: "application/x-ldjson",
            cls.NDJSON: ContentType.NDJSON.value,
            cls.ODS: ContentType.ODS.value,
            cls.PARQUET: ContentType.PARQUET.value,
            cls.XLSX: ContentType.XLSX.value,
        }
        v2 = mapping[v1]
        return v2
