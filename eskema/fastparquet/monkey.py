import fastparquet.core

from eskema.fastparquet.core import read_col


def activate():
    fastparquet.core.read_col = read_col
