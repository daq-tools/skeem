# How many bytes to read from input data.
from eskema.type import ContentType

PEEK_BYTES = 10000

# How many lines to read from input data.
PEEK_LINES = 1000

# Which content types to route to the "frictionless" backend.
FRICTIONLESS_CONTENT_TYPES = [
    ContentType.PARQUET,
]
