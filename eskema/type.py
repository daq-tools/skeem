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

    # Primary definitions.
    CSV = "text/csv"
    JSON = "application/json"
    NDJSON = "application/x-ndjson"
    LDJSON = "application/x-ldjson"

    # Secondary aliases.
    JSONL = "application/x-ndjson"

    @classmethod
    def from_filename(cls, filename: t.Union[Path, str]) -> "ContentType":
        mimetype, _ = mimetypes.guess_type(filename)
        return cls(mimetype)

    @classmethod
    def from_name(cls, name: str) -> "ContentType":
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
        if type_ in [ContentType.NDJSON, ContentType.JSONL, ContentType.LDJSON]:
            return True
        else:
            return False

    @classmethod
    def to_suffix(cls, type_: "ContentType") -> str:
        if cls.is_ndjson(type_):
            return ".ndjson"
        elif type_ is ContentType.CSV:
            return ".csv"
        elif type_ is ContentType.JSON:
            return ".json"
        else:
            raise ValueError(f"Unable to compute suffix for content type '{type_}'")


class ContentTypeShort(Enum):

    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"
    LDJSON = "ldjson"
    NDJSON = "ndjson"

    @classmethod
    def resolve(cls, label: str) -> str:
        v1 = cls(label)
        mapping = {
            cls.CSV: "text/csv",
            cls.JSON: "application/json",
            cls.JSONL: "application/x-ndjson",
            cls.LDJSON: "application/x-ldjson",
            cls.NDJSON: "application/x-ndjson",
        }
        v2 = mapping[v1]
        return v2
