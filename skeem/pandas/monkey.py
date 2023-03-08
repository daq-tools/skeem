import pandas.io.common

from skeem.pandas.compat import fix_optional_dependency_list
from skeem.pandas.io_common import _get_filepath_or_buffer


def activate():
    fix_optional_dependency_list()
    pandas.io.common._get_filepath_or_buffer = _get_filepath_or_buffer
