import io
import logging
import typing as t

import pandas as pd

from eskema.io import json_get_first_records
from eskema.settings import PEEK_LINES
from eskema.type import ContentType

IntOrString = t.TypeVar("IntOrString", int, str)
AddressType = t.Union[int, str, t.List[IntOrString]]

# Primary list of field name prefixes to consider as primary key.
PK_CANDIDATES_PRIMARY_PREFIXES = ["id"]

# Primary list of absolute field names to consider as primary key.
PK_CANDIDATES_PRIMARY_LIST = ["pk", "key"]

# Secondary list of absolute field names to consider as primary key.
PK_CANDIDATES_SECONDARY_ENGLISH = ["#", "number", "nr"]
PK_CANDIDATES_SECONDARY_GERMAN = ["nummer", "no", "kennung", "bezeichner", "identifikator"]
PK_CANDIDATES_SECONDARY_LIST = PK_CANDIDATES_SECONDARY_ENGLISH + PK_CANDIDATES_SECONDARY_GERMAN


logger = logging.getLogger(__name__)


def infer_pk(
    data: t.Any, content_type: t.Optional[ContentType] = None, address: t.Optional[AddressType] = None
) -> t.Optional[str]:
    """
    Attempt to infer primary key from column names and data, DWIM [1].

    [1] https://en.wikipedia.org/wiki/DWIM
    """
    pk = _infer_pk(data, content_type, address)
    logger.info(f"Inferred primary key: {pk}")
    if hasattr(data, "seek"):
        data.seek(0)
    return pk


def _infer_pk(
    data: t.Any, content_type: t.Optional[ContentType] = None, address: t.Optional[AddressType] = None
) -> t.Optional[str]:

    if isinstance(data, pd.DataFrame):
        df = data
    else:
        if content_type is None:
            raise ValueError("Unable to infer primary key without content type")
        if isinstance(data, str):
            data = io.StringIO(data)
        df = to_dataframe(data=data, content_type=content_type, address=address)

    # Decode list of column names.
    columns = list(df.columns)
    logger.info(f"Decoded list of column names: {columns}")

    # If there is any column starting with "id", use it as primary key right away.
    for column in columns:
        for candidate in PK_CANDIDATES_PRIMARY_PREFIXES:
            if column.lower().startswith(candidate):
                return column
    for column in columns:
        for candidate in PK_CANDIDATES_PRIMARY_LIST:
            if column.lower() == candidate:
                return column

    # Choose primary key based on a list of other candidates.
    for column in columns:
        if column.lower() in PK_CANDIDATES_SECONDARY_LIST:
            return column

    # If the values of the first column are unique, use that as primary key.
    column1_series = df[df.columns[0]]
    if column1_series.dtype not in ["datetime64[ns]", "float64"] and column1_series.is_unique:
        return df.columns[0]

    return None


def to_dataframe(data: t.Any, content_type: ContentType, address: t.Optional[AddressType] = None) -> pd.DataFrame:
    # Only peek at the first lines of data.
    if ContentType.is_ndjson(content_type):
        df = pd.read_json(data, lines=True, nrows=PEEK_LINES)
    elif content_type is ContentType.CSV:
        df = pd.read_csv(data, nrows=PEEK_LINES)
    elif content_type in [ContentType.XLSX, ContentType.ODS]:
        sheet_name = address or 0
        df = pd.read_excel(data, sheet_name=sheet_name, nrows=PEEK_LINES)

    # Only load the first record(s) from a regular JSON document.
    elif content_type is ContentType.JSON:
        records = json_get_first_records(data, nrecords=PEEK_LINES)
        df = pd.DataFrame.from_records(data=records)

    # Croak otherwise.
    else:
        raise NotImplementedError(f"Inferring primary key with content type '{content_type}' not implemented yet")

    return df
