from pathlib import Path

import pytest


@pytest.fixture
def ndjson_file_basic():
    return Path("tests/testdata/basic.ndjson")
