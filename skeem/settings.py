from skeem.type import ContentType

# How many lines to read from input data.
PEEK_LINES = 100

# How many bytes to read from input data.
PEEK_BYTES = PEEK_LINES * 130

# Which content types to route to the "frictionless" backend.
FRICTIONLESS_CONTENT_TYPES = [
    ContentType.PARQUET,
]
