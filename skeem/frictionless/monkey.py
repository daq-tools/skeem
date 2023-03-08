from .loader_s3 import read_byte_stream_create as s3_read_byte_stream_create
from .loader_stream import read_byte_stream_create
from .pandas_plugin import create_parser
from .parser_jsonl import read_cell_stream_create
from .resource import ResourcePlus


def activate():
    patch_core()
    patch_modules()


def patch_core():
    """
    Override sample size for all `frictionless.Resource` instances.
    """
    import frictionless

    frictionless.resource.Resource = ResourcePlus
    frictionless.Resource = ResourcePlus


def patch_modules():
    """
    Enhance `frictionless` loader and parser modules.

    - Apply sample size to pandas parser as well.
    - Don't croak when reading streams without `name` attribute.
    """

    import frictionless.formats.json.parsers
    import frictionless.formats.pandas.plugin
    import frictionless.schemes.aws.loaders.s3
    import frictionless.schemes.stream.loader

    frictionless.formats.json.parsers.JsonlParser.read_cell_stream_create = read_cell_stream_create
    frictionless.formats.pandas.plugin.PandasPlugin.create_parser = create_parser
    frictionless.schemes.aws.loaders.s3.S3Loader.read_byte_stream_create = s3_read_byte_stream_create
    frictionless.schemes.stream.loader.StreamLoader.read_byte_stream_create = read_byte_stream_create
