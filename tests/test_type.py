import pytest

from eskema.exception import UnknownContentType
from eskema.type import ContentType, ContentTypeMime, ContentTypeSuffix

# ===============
# Main test cases
# ===============


@pytest.mark.parametrize("name", ["ndjson", "NDJSON", "application/x-ndjson"])
def test_content_type_from_name_success(name: str):
    assert ContentType.from_name(name) is ContentType.NDJSON


@pytest.mark.parametrize("filename", ["test.lp", "test.lineprotocol"])
def test_content_type_from_filename_lineprotocol(filename: str):
    assert ContentType.from_filename(filename) is ContentType.LINEPROTOCOL


@pytest.mark.parametrize("filename", ["test.nc", "test.netcdf"])
def test_content_type_from_filename_netcdf(filename: str):
    assert ContentType.from_filename(filename) is ContentType.NETCDF


def test_content_type_to_suffix_lineprotocol():
    assert ContentType.LINEPROTOCOL.suffix == ".lp"


def test_content_type_to_suffix_netcdf():
    assert ContentType.NETCDF.suffix == ".nc"


@pytest.mark.parametrize("label", ["NDJSON", "JSONL", "LDJSON"])
def test_content_type_to_suffix_ndjson_aliases(label: str):
    assert ContentType(label).suffix == ".ndjson"


def test_content_type_suffix_from_label_success():
    assert ContentTypeSuffix.from_label(".netcdf") is ContentTypeSuffix.NETCDF


def test_content_type_suffix_content_type_success():
    assert ContentTypeSuffix["GRIB2"].content_type is ContentType.GRIB2


def test_content_type_suffix_label_success():
    assert ContentTypeSuffix["GRIB2"].label == ".grib2"


# ============================
# Test cases for unknown slots
# ============================


def test_content_type_unknown_key():
    with pytest.raises(KeyError) as ex:
        _ = ContentType["UNKNOWN"]
    assert ex.match("'UNKNOWN'")


def test_content_type_unknown_value():
    with pytest.raises(ValueError) as ex:
        ContentType("UNKNOWN")
    assert ex.match("'UNKNOWN' is not a valid ContentType")


def test_content_type_from_name_unknown():
    with pytest.raises(ValueError) as ex:
        ContentType.from_name("unknown")
    assert ex.match("'unknown' is not a valid ContentType or ContentTypeMime")


def test_content_type_from_filename_unknown():
    with pytest.raises(UnknownContentType) as ex:
        ContentType.from_filename("test.unknown")
    assert ex.match("Unable to guess content type from 'test.unknown'")


def test_content_type_suffix_unknown_value():
    with pytest.raises(ValueError) as ex:
        ContentTypeSuffix(".unknown")
    assert ex.match("'.unknown' is not a valid ContentTypeSuffix")


def test_content_type_suffix_from_label_unknown():
    with pytest.raises(ValueError) as ex:
        ContentTypeSuffix.from_label(".unknown")
    assert ex.match("'.unknown' is not a valid ContentTypeSuffix")


def test_content_type_mime_unknown_value():
    with pytest.raises(ValueError) as ex:
        ContentTypeMime("application/vnd.acme.unknown")
    assert ex.match("'application/vnd.acme.unknown' is not a valid ContentTypeMime")
