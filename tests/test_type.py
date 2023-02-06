import pytest

from eskema.type import ContentType


def test_content_type_no_suffix():
    with pytest.raises(ValueError) as ex:
        ContentType.to_suffix("foo")
    assert ex.match("Unable to compute suffix for content type 'foo'")
