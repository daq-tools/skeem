import fsspec.spec

from eskema.fsspec.spec import readlines


def activate():
    fsspec.spec.AbstractBufferedFile.readlines = readlines
