import datetime
from decimal import Decimal, InvalidOperation

import dateutil
import ddlgenerator.ddlgenerator
import ddlgenerator.typehelpers
import sqlalchemy as sa
from ddlgenerator.ddlgenerator import _dump
from ddlgenerator.reshape import _illegal_in_column_name
from ddlgenerator.typehelpers import _complex_enough_to_be_date, _digits_only


def coerce_to_specific(datum):
    """
    Coerces datum to the most specific data type possible
    Order of preference: datetime, boolean, integer, decimal, float, string

    >>> coerce_to_specific('-000000001854.60')
    Decimal('-1854.60')
    >>> coerce_to_specific(7.2)
    Decimal('7.2')
    >>> coerce_to_specific("Jan 17 2012")
    datetime.datetime(2012, 1, 17, 0, 0)
    >>> coerce_to_specific("something else")
    'something else'
    >>> coerce_to_specific("20141010")
    datetime.datetime(2014, 10, 10, 0, 0)
    >>> coerce_to_specific("001210107")
    1210107
    >>> coerce_to_specific("010")
    10
    >>> coerce_to_specific(0)
    0
    >>> coerce_to_specific(1)
    1
    >>> coerce_to_specific("yes")
    True
    >>> coerce_to_specific("no")
    False
    >>> coerce_to_specific(None)
    """
    if datum is None:
        return None
    try:
        result = dateutil.parser.parse(datum)
        # but even if this does not raise an exception, may
        # not be a date -- dateutil's parser is very aggressive
        # check for nonsense unprintable date
        str(result)
        # most false date hits will be interpreted as times today
        # or as unlikely far-future or far-past years
        clean_datum = datum.strip().lstrip("-").lstrip("0").rstrip(".")
        if len(_complex_enough_to_be_date.findall(clean_datum)) < 2:
            digits = _digits_only.search(clean_datum)
            if (not digits) or (len(digits.group(0)) not in (4, 6, 8, 12, 14, 17)):
                raise Exception("false date hit for %s" % datum)
            if result.date() == datetime.datetime.now().date():
                raise Exception("false date hit (%s) for %s" % (str(result), datum))
            if not (1700 < result.year < 2150):
                raise Exception("false date hit (%s) for %s" % (str(result), datum))
        return result
    except Exception:
        pass
    try:
        return int(str(datum))
    except ValueError:
        pass
    try:
        return Decimal(str(datum))
    except InvalidOperation:
        pass
    try:
        return float(str(datum))
    except ValueError:
        pass
    if str(datum).strip().lower() in ("0", "false", "f", "n", "no"):
        return False
    elif str(datum).strip().lower() in ("1", "true", "t", "y", "yes"):
        return True
    return str(datum)


class AnyDialect(dict):
    """
    Make `ddlgenerator` accept any dialect, to let SQLAlchemy decide
    whether it is supported or not.

    >>> dd = AnyDialect()

    >>> dd["postgresql"]
    <sqlalchemy.engine.mock.MockConnection object at ...>

    >>> "foo" in dd
    True

    >>> dd["foo"]
    Traceback (most recent call last):
    ...
    sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:foo
    """

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return sa.create_mock_engine(f"{item}://", executor=_dump)


def clean_key_name(key):
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
    result = sa.sql.quoted_name(result, quote='"')
    return result


def activate():
    ddlgenerator.typehelpers.coerce_to_specific = coerce_to_specific
    ddlgenerator.ddlgenerator.mock_engines = AnyDialect()
    ddlgenerator.reshape.clean_key_name = clean_key_name
