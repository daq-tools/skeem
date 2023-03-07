import pandas.io.common

from eskema.pandas.compat import fix_optional_dependency_list
from eskema.pandas.io_common import _get_filepath_or_buffer


def activate():
    fix_optional_dependency_list()
    pandas.io.common._get_filepath_or_buffer = _get_filepath_or_buffer
