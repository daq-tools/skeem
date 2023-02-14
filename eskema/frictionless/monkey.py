import frictionless.schemes.stream.loader

from .stream_loader import read_byte_stream_create


def activate():

    frictionless.schemes.stream.loader.StreamLoader.read_byte_stream_create = read_byte_stream_create
