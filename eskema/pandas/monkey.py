import pandas.io.common

from eskema.pandas.io_common import _get_filepath_or_buffer


def activate():
    pandas.io.common._get_filepath_or_buffer = _get_filepath_or_buffer
