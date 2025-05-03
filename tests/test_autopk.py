import re

import pytest

from skeem.autopk import infer_pk
from skeem.types import ContentType


def test_autopk_content_type_invalid_none():
    """
    Inferring the primary key without content type croaks.
    """
    with pytest.raises(ValueError) as ex:
        infer_pk("", None)
    assert ex.match("Unable to infer primary key without content type")


def test_autopk_content_type_invalid_str():
    """
    Inferring the primary key using an invalid content type croaks.
    """
    with pytest.raises(TypeError) as ex:
        infer_pk("", "foo")
    assert ex.match(
        re.escape("Failed to infer primary key with invalid content type (value=foo, type=str), expected `ContentType`")
    )


def test_autopk_content_type_ignored():
    """
    Inferring the primary key from a content type listed as `NO_AUTOPK` yields `None`.
    """
    assert infer_pk("", ContentType.GRIB2) is None


def test_autopk_content_type_unknown():
    """
    Inferring the primary key using a content type not implemented yet, croaks correspondingly.
    """
    with pytest.raises(NotImplementedError) as ex:
        infer_pk("", ContentType.PARQUET)
    assert ex.match("Failed to infer primary key. Reason: Unable to process content type: ContentType.PARQUET")
