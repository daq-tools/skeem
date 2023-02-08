import mimetypes
import typing as t
from enum import Enum
from pathlib import Path


def init():
    """
    Add NDJSON variants to MIME types map.

    Table comparing NDJSON (ex. LDJSON) and JSON Lines side-by-side:
    https://github.com/ndjson/ndjson.github.io/issues/1#issuecomment-109935996
    """
    mimetypes.init()
    mimetypes.types_map.update(
        {
            ".ndjson": "application/x-ndjson",
            ".jsonl": "application/x-ndjson",
            ".ldjson": "application/x-ldjson",
            ".ldj": "application/x-ldjson",
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
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ODS = "application/vnd.oasis.opendocument.spreadsheet"

    # Secondary aliases.
    LDJSON = "application/x-ldjson"
    JSONL = "application/x-ndjson"

    @classmethod
    def from_filename(cls, filename: t.Union[Path, str]) -> "ContentType":
        """
        Derive content type from filename extension.

        >>> ContentType.from_filename("foo.csv")
        <ContentType.CSV: 'text/csv'>
        """
        mimetype, _ = mimetypes.guess_type(filename)
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
        if cls.is_ndjson(type_):
            return ".ndjson"
        elif type_ is ContentType.CSV:
            return ".csv"
        elif type_ is ContentType.JSON:
            return ".json"
        elif type_ is ContentType.XLSX:
            return ".xlsx"
        elif type_ is ContentType.ODS:
            return ".ods"
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
    XLSX = "xlsx"

    @classmethod
    def resolve(cls, label: str) -> str:
        v1 = cls(label)
        mapping = {
            cls.CSV: "text/csv",
            cls.JSON: "application/json",
            cls.JSONL: "application/x-ndjson",
            cls.LDJSON: "application/x-ldjson",
            cls.NDJSON: "application/x-ndjson",
            cls.ODS: ContentType.ODS.value,
            cls.XLSX: ContentType.XLSX.value,
        }
        v2 = mapping[v1]
        return v2
