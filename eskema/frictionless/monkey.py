from .pandas_plugin import create_parser
from .resource import ResourcePlus
from .stream_loader import read_byte_stream_create


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

    import frictionless.formats.pandas.plugin
    import frictionless.schemes.stream.loader

    frictionless.formats.pandas.plugin.PandasPlugin.create_parser = create_parser
    frictionless.schemes.stream.loader.StreamLoader.read_byte_stream_create = read_byte_stream_create
