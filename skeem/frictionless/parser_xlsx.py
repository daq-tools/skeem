import atexit
import os
import shutil
import tempfile

from frictionless.formats.excel.control import ExcelControl
from frictionless.resource.resource import Resource
from frictionless.system import system


def read_loader(self):
    """
    Patched for Python 3.12.

    https://github.com/frictionlessdata/frictionless-py/issues/1642
    https://github.com/frictionlessdata/frictionless-py/pull/1684
    """
    control = ExcelControl.from_dialect(self.resource.dialect)
    loader = system.create_loader(self.resource)
    if not loader.remote:
        return loader.open()

    # Remote
    # Create copy for remote source
    # For remote stream we need local copy (will be deleted on close by Python)
    # https://docs.python.org/3.5/library/tempfile.html#tempfile.TemporaryFile
    if loader.remote:
        path = self.resource.normpath

        # Cached
        if control.workbook_cache is not None and path in control.workbook_cache:
            # TODO: rebase on using resource without system?
            resource = Resource(path, scheme="file", format="xlsx")
            resource.infer(sample=False)
            loader = system.create_loader(resource)
            return loader.open()

        with loader as loader:
            delete = control.workbook_cache is None
            target = tempfile.NamedTemporaryFile(delete=delete)
            shutil.copyfileobj(loader.byte_stream, target)
            target.seek(0)
        if not delete:
            control.workbook_cache[path] = target.name  # type: ignore
            atexit.register(os.remove, target.name)
        # TODO: rebase on using resource without system?
        resource = Resource(target, scheme="stream", format="xlsx")
        resource.infer(sample=False)
        loader = system.create_loader(resource)
        return loader.open()

    return None
