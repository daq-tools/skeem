import pandas as pd

PK_CANDIDATES_PRIMARY_PREFIXES = ["id"]
PK_CANDIDATES_PRIMARY_LIST = ["pk", "key"]

PK_CANDIDATES_SECONDARY_ENGLISH = ["#", "number", "nr"]
PK_CANDIDATES_SECONDARY_GERMAN = ["nummer", "no", "kennung", "bezeichner", "identifikator"]
PK_CANDIDATES_SECONDARY = PK_CANDIDATES_SECONDARY_ENGLISH + PK_CANDIDATES_SECONDARY_GERMAN


def infer_pk(data):
    """
    Attempt to infer primary key from column names and data.

    Aims to implement the algorithm to DWIM [1].

    [1] https://en.wikipedia.org/wiki/DWIM
    """
    # Look at the first 1000 lines worth of data.
    df = pd.read_json(data, lines=True, nrows=1000)
    columns = list(df.columns)

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
