import io
import re
import typing as t

import pytest

from eskema.model import Resource


@pytest.mark.parametrize("indata", ["foo", b"foo", io.StringIO("foo"), io.BytesIO(b"foo")])
def test_resource_peek_data(indata: t.Union[t.ByteString]):
    resource = Resource(data=indata)
    assert resource.peek().read() == b"foo"


def test_resource_peek_empty():
    resource = Resource(data="")
    assert resource.peek().read() == b""


def test_resource_peek_none():
    resource = Resource(data=None)
    with pytest.raises(ValueError) as ex:
        resource.peek()
    assert ex.match("Unable to open resource: Resource(.+)")


def test_resource_peek_file_success(tmp_path):
    tmp_file = tmp_path.joinpath("tmpfile.txt")
    tmp_file.write_text("foo")
    resource = Resource(path=tmp_file)
    assert resource.peek().read() == b"foo"


def test_resource_peek_file_failure():
    resource = Resource(path="/tmp/foo/non-existent.csv")  # noqa: S108
    with pytest.raises(FileNotFoundError) as ex:
        resource.peek()
    assert ex.match(re.escape("[Errno 2] No such file or directory: '/tmp/foo/non-existent.csv'"))


def test_resource_peek_url_success_csv(csv_url_basic):
    resource = Resource(path=csv_url_basic)
    assert (
        resource.peek().read()
        == b'id,name,date,fruits,price\n1,"foo","2014-10-31T09:22:56","apple,banana",0.42\n2,"bar",,"pear",0.84'
    )


def test_resource_peek_url_success_html():
    resource = Resource(path="https://example.org/")
    assert resource.peek().read().startswith(b"<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>")


def test_resource_peek_url_failure_404():
    resource = Resource(path="https://example.org/foo.csv")
    with pytest.raises(FileNotFoundError) as ex:
        resource.peek()
    assert ex.match(re.escape("https://example.org/foo.csv"))


def test_resource_peek_url_failure_host_not_found():
    resource = Resource(path="https://example-unknown.org/foo.csv")
    with pytest.raises(FileNotFoundError) as ex:
        resource.peek()
    assert ex.match(re.escape("https://example-unknown.org/foo.csv"))
