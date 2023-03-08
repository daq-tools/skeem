import fastparquet.core

from skeem.fastparquet.core import read_col


def activate():
    fastparquet.core.read_col = read_col
