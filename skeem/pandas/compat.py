import pandas.compat._optional


def fix_optional_dependency_list():
    """
    Work around `ImportError: Can't determine version for hypothesis`.
    """
    try:
        del pandas.compat._optional.VERSIONS["hypothesis"]
    except KeyError:
        pass
