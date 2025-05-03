import mimetypes
import typing as t
from collections import OrderedDict
from enum import Enum
from pathlib import Path

from skeem.exception import UnknownContentType
from skeem.util.data import enum_values


def init():
    """
    Expand Python's MIME types map.

    Table comparing NDJSON (ex. LDJSON) and JSON Lines side-by-side:
    https://github.com/ndjson/ndjson.github.io/issues/1#issuecomment-109935996

    The listed MIME types are not officially registered, for some of them,
    there are a few hints, for others, the MIME type has been completely made up.

    - Parquet: https://issues.apache.org/jira/browse/PARQUET-1889?focusedCommentId=17468854#comment-17468854
    - GRIB: https://github.com/wmo-im/GRIB2/issues/175#issuecomment-1359209980
    """
    mimetypes.init()
    mimetypes.types_map.update(
        {
            ".grib2": "application/x-grib2",
            ".gz": "application/gzip",
            ".jsonl": "application/x-ndjson",
            ".ldjson": "application/x-ldjson",
            ".ldj": "application/x-ldjson",
            ".lineprotocol": "application/vnd.influxdata.lineprotocol",
            ".lp": "application/vnd.influxdata.lineprotocol",
            ".ndjson": "application/x-ndjson",
            ".netcdf": "application/x-netcdf",
            ".parquet": "application/vnd.apache.parquet",
            ".parq": "application/vnd.apache.parquet",
            ".pq": "application/vnd.apache.parquet",
        }
    )


class ContentType(Enum):
    """
    Manage supported content types and provide support methods.
    """

    # Primary definitions.
    CSV = "CSV"
    GRIB2 = "GRIB2"
    JSON = "JSON"
    NETCDF = "NETCDF"
    NDJSON = "NDJSON"
    LINEPROTOCOL = "LINEPROTOCOL"
    ODS = "ODS"
    PARQUET = "PARQUET"
    XLSX = "XLSX"

    # Secondary aliases.
    JSONL = "JSONL"
    LDJSON = "LDJSON"

    # Archive formats.
    GZIP = "GZIP"

    @classmethod
    def values(cls):
        return enum_values(cls)

    @classmethod
    def from_name(cls, name: str) -> "ContentType":
        """
        Derive content type from name or mime type.

        >>> ContentType.from_name("csv")
        <ContentType.CSV: 'CSV'>

        >>> ContentType.from_name("CSV")
        <ContentType.CSV: 'CSV'>

        >>> ContentType.from_name("text/csv")
        <ContentType.CSV: 'CSV'>
        """

        try:
            return ContentType(name.upper())
        except ValueError:
            pass

        try:
            return ContentTypeMime(name).content_type
        except ValueError:
            pass

        raise ValueError(f"'{name}' is not a valid ContentType or ContentTypeMime")

    @classmethod
    def from_filename(cls, filename: t.Union[Path, str]) -> "ContentType":
        """
        Derive content type from filename extension.

        >>> ContentType.from_filename("foo.csv")
        <ContentType.CSV: 'CSV'>
        """
        mimetype: t.Union[str, None]
        filename = str(filename)
        if filename.endswith(".gz"):
            mimetype = "application/gzip"
        else:
            mimetype, _ = mimetypes.guess_type(filename, strict=False)
        if mimetype is None:
            raise UnknownContentType(f"Unable to guess content type from '{filename}'")
        return ContentTypeMime(mimetype).content_type

    @property
    def suffix(self) -> str:
        """
        Derive filename extension from content type.
        """
        type_ = self

        if type_.is_ndjson():
            type_ = ContentType.NDJSON

        suffix: ContentTypeSuffix = ContentTypeSuffix[type_.name]
        return suffix.label

    def is_ndjson(self) -> bool:
        """
        Whether the content type is NDJSON or alike.
        """
        return self in ContentTypeGroup.NDJSON_ALIASES


class ContentTypeMime(Enum):
    """
    Manage content type -> mime type mapping.
    """

    # Primary definitions.
    CSV = "text/csv"
    GRIB2 = "application/x-grib2"
    JSON = "application/json"
    NETCDF = "application/x-netcdf"
    NDJSON = "application/x-ndjson"
    LINEPROTOCOL = "application/vnd.influxdata.lineprotocol"
    ODS = "application/vnd.oasis.opendocument.spreadsheet"
    PARQUET = "application/vnd.apache.parquet"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Secondary aliases.
    JSONL = "application/x-ndjson"
    LDJSON = "application/x-ldjson"

    # Archive formats.
    GZIP = "application/gzip"

    @classmethod
    def values(cls):
        return enum_values(cls)

    @property
    def content_type(self) -> ContentType:
        """
        Return corresponding `ContentType`.
        """
        return ContentType.from_name(self.name)


class ContentTypeSuffix(Enum):
    """
    Manage content type -> file extension suffix mapping.
    """

    CSV = [".csv"]
    GRIB2 = [".grib2"]
    JSON = [".json"]
    JSONL = [".jsonl"]
    LDJSON = [".ldjson"]
    LINEPROTOCOL = [".lp", ".lineprotocol"]
    NETCDF = [".nc", ".netcdf"]
    NDJSON = [".ndjson"]
    ODS = [".ods"]
    PARQUET = [".parquet"]
    XLSX = [".xlsx"]

    @classmethod
    def values(cls):
        return enum_values(cls)

    @classmethod
    def from_label(cls, label: str) -> "ContentTypeSuffix":
        """
        Derive `ContentTypeSuffix` from file extension suffix string.
        """
        for item in cls:
            if label in item.value:
                return item
        raise ValueError(f"'{label}' is not a valid ContentTypeSuffix")

    @property
    def content_type(self) -> ContentType:
        """
        Return corresponding `ContentType`.
        """
        return ContentType.from_name(self.name)

    @property
    def label(self) -> str:
        """
        The first slot of the enum value is the canonical file extension suffix.
        """
        return self.value[0]


class ContentTypeGroup:
    """
    Groups of content types for different purposes.
    """

    # Primary key detection will not be invoked for those content types.
    NO_AUTOPK = [
        ContentType.GRIB2,
        ContentType.NETCDF,
    ]

    # All "binary" files must not be read partially, but as a whole instead.
    NO_PARTIAL = [
        ContentType.GRIB2,
        ContentType.NETCDF,
        ContentType.ODS,
        ContentType.XLSX,
    ]

    # All types which should be treated equally to NDJSON.
    NDJSON_ALIASES = [
        ContentType.JSONL,
        ContentType.LDJSON,
        ContentType.NDJSON,
    ]


class TypeInfo:
    @classmethod
    def get(cls):
        metadata = OrderedDict()
        metadata["Content types"] = ContentType.values()
        metadata["MIME types"] = ContentTypeMime.values()
        metadata["File suffixes"] = ContentTypeSuffix.values()
        return metadata
