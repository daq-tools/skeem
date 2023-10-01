import datetime
import typing as t
from decimal import Decimal, InvalidOperation

import dateutil.parser
import pandas as pd
from ddlgenerator.typehelpers import _complex_enough_to_be_date, _digits_only

CoercionType = t.Union[str, int, float, bool, Decimal, datetime.datetime]


def coerce_to_specific(datum: CoercionType) -> t.Optional[CoercionType]:
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

    A few additional test cases.

    >>> coerce_to_specific(None)
    >>> coerce_to_specific(pd.NA)
    >>> coerce_to_specific(pd.NaT)

    >>> coerce_to_specific(pd.Timestamp(None))
    >>> coerce_to_specific(pd.Timestamp(pd.NaT))
    >>> coerce_to_specific(pd.Timestamp("2014-10-31T09:22:56"))
    datetime.datetime(2014, 10, 31, 9, 22, 56)

    >>> coerce_to_specific("0704.0001")
    Decimal('704.0001')
    """
    if datum is None or pd.isna(datum):
        return None
    try:
        if isinstance(datum, pd.Timestamp):
            datum = str(datum)

        if isinstance(datum, (bytes, str, t.IO)):
            result = dateutil.parser.parse(datum)
            # but even if this does not raise an exception, may
            # not be a date -- dateutil's parser is very aggressive
            # check for nonsense unprintable date
            str(result)

            # most false date hits will be interpreted as times today
            # or as unlikely far-future or far-past years
            if isinstance(datum, str):
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
    except Exception:  # noqa: S110
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


def best_coercable(data):
    """
    Given an iterable of scalar data, returns the datum representing the most specific
    data type the list overall can be coerced into, preferring datetimes, then bools,
    then integers, then decimals, then floats, then strings.

    >>> best_coercable((6, '2', 9))
    6
    >>> best_coercable((Decimal('6.1'), 2, 9))
    Decimal('6.1')
    >>> best_coercable(('2014 jun 7', '2011 may 2'))
    datetime.datetime(2014, 6, 7, 0, 0)
    >>> best_coercable((7, 21.4, 'ruining everything'))
    'ruining everything'
    >>> best_coercable(("0704.0001",))
    '0704.0001'
    """
    from ddlgenerator.typehelpers import worst_decimal

    preference = (datetime.datetime, bool, int, Decimal, float, str)
    worst_pref = 0
    worst = ""
    for datum in data:
        coerced_candidate = coerce_to_specific(datum)

        # PATCH: Decimals like `"0704.0001"` should be treated as strings, see `nested.json`.
        if isinstance(datum, str) and isinstance(coerced_candidate, Decimal):
            coerced = datum
        else:
            coerced = coerced_candidate

        pref = preference.index(type(coerced))
        if pref > worst_pref:
            worst_pref = pref
            worst = coerced
        elif pref == worst_pref:
            if isinstance(coerced, Decimal):
                worst = worst_decimal(coerced, worst)
            elif isinstance(coerced, float):
                worst = max(coerced, worst)
            else:  # int, str
                if len(str(coerced)) > len(str(worst)):
                    worst = coerced
    # print("worst:", worst, type(worst))  # noqa: ERA001
    return worst
