import pytest

from eskema.autopk import infer_pk


def test_autopk_unknown_content_type():
    """
    Verify that inferring the primary key without content type is not possible.
    """
    with pytest.raises(NotImplementedError) as ex:
        infer_pk("", "foo")
    assert ex.match("Inferring primary key with content type 'foo' not implemented yet")
