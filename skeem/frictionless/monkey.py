from .loader_s3 import read_byte_stream_create as s3_read_byte_stream_create
from .loader_stream import read_byte_stream_create
from .pandas_plugin import create_parser
from .parser_jsonl import read_cell_stream_create


def activate():
    patch_modules()


def patch_modules():
    """
    Enhance `frictionless` loader and parser modules.

    - Apply sample size to pandas parser as well.
    - Don't croak when reading streams without `name` attribute.
    """

    import frictionless.formats.excel.parsers
    import frictionless.schemes.aws.loaders.s3
    import frictionless.schemes.stream.loader

    frictionless.formats.JsonlParser.read_cell_stream_create = read_cell_stream_create
    frictionless.formats.pandas.plugin.PandasPlugin.create_parser = create_parser
    frictionless.schemes.aws.loaders.s3.S3Loader.read_byte_stream_create = s3_read_byte_stream_create
    frictionless.schemes.stream.loader.StreamLoader.read_byte_stream_create = read_byte_stream_create
