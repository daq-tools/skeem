import sqlalchemy as sa
from ddlgenerator.reshape import UniqueKey, _illegal_in_column_name, all_values_for


def clean_key_name(key: str) -> str:
    """
    Makes ``key`` a valid and appropriate SQL column name:

    1. Replaces illegal characters in column names with ``_``

    2. Prevents name from beginning with a digit (prepends ``_``)

    3. Lowercases name.  If you want case-sensitive table
    or column names, you are a bad person, and you should feel bad.

    >>> clean_key_name("foo-bar")
    'foo_bar'

    >>> clean_key_name("1")
    '_1'

    >>> clean_key_name(42.42)
    '_42_42'

    >>> clean_key_name("date")
    'date'
    """
    result = _illegal_in_column_name.sub("_", str(key).strip())
    if result[0].isdigit():
        result = "_%s" % result
    # Patch: Not necessarily needed? In our case, we don't want `date` to be renamed to `_date`.
    # if result.upper() in sql_reserved_words:
    result = result.lower()
    # Patch: Just to make sure?
    result = sa.sql.quoted_name(result, quote=True)
    return result


def use_this_pk(self, pk_name, key_type):
    """
    More graceful version which will ignore errors on `int` type PKs,
    and fall back to the effective type instead.
    """
    if key_type is int:
        try:
            all_max = max([0] + all_values_for(self, pk_name))
            self.pk = UniqueKey(pk_name, key_type, max=all_max)
            return
        except TypeError:
            pass

    self.pk = UniqueKey(pk_name, key_type)
