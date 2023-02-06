import io
import logging
import typing as t

import pandas as pd

from eskema.type import ContentType

PK_CANDIDATES_PRIMARY_PREFIXES = ["id"]
PK_CANDIDATES_PRIMARY_LIST = ["pk", "key"]

PK_CANDIDATES_SECONDARY_ENGLISH = ["#", "number", "nr"]
PK_CANDIDATES_SECONDARY_GERMAN = ["nummer", "no", "kennung", "bezeichner", "identifikator"]
PK_CANDIDATES_SECONDARY = PK_CANDIDATES_SECONDARY_ENGLISH + PK_CANDIDATES_SECONDARY_GERMAN

PEEK_LINES = 1000


logger = logging.getLogger(__name__)


def infer_pk(data: t.Any, content_type: ContentType) -> t.Optional[str]:
    """
    Attempt to infer primary key from column names and data, DWIM [1].

    [1] https://en.wikipedia.org/wiki/DWIM
    """
    pk = _infer_pk(data, content_type)
    logger.info(f"Inferred primary key: {pk}")
    return pk


def _infer_pk(data: t.Any, content_type: ContentType) -> t.Optional[str]:
    """
    Attempt to infer primary key from column names and data, DWIM [1].

    [1] https://en.wikipedia.org/wiki/DWIM
    """

    if isinstance(data, str):
        data = io.StringIO(data)

    # Only peek at the first lines of data.
    if ContentType.is_ndjson(content_type):
        df = pd.read_json(data, lines=True, nrows=PEEK_LINES)
    elif content_type is ContentType.CSV:
        df = pd.read_csv(data, nrows=PEEK_LINES)
    else:
        raise NotImplementedError(f"Inferring primary key with content type '{content_type}' not implemented yet")

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
        if column.lower() in PK_CANDIDATES_SECONDARY:
            return column

    # If the values of the first column are unique, use that as primary key.
    column1_series = df[df.columns[0]]
    if column1_series.is_unique:
        return df.columns[0]

    return None
