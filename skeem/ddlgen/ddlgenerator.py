import datetime as dt
import logging
import pprint
from collections import OrderedDict
from decimal import Decimal

import sqlalchemy as sa
from ddlgenerator.ddlgenerator import Table, _dump

try:
    import ddlgenerator.typehelpers as th
except ImportError:  # pragma: no cover
    import typehelpers as th  # TODO: can py2/3 split this


logger = logging.getLogger(__name__)


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

    def __contains__(self, item) -> bool:
        return True

    def __getitem__(self, item):
        return sa.create_mock_engine(f"{item}://", executor=_dump)


class TablePlus(Table):
    """
    Overwrite specific methods with a few patches.
    """

    def _determine_types(self):
        column_data = OrderedDict()  # noqa: F841
        self.columns = OrderedDict()
        if hasattr(self.data, "generator") and hasattr(self.data.generator, "sqla_columns"):
            for col in self.data.generator.sqla_columns:
                self.columns[col.name] = {
                    "is_nullable": col.nullable,
                    "is_unique": col.unique,
                    "satype": col.type,
                    "pytype": col.pytype,
                }
            return
        self.comments = {}
        rowcount = 0
        for row in self.data:
            rowcount += 1
            keys = row.keys()
            # print("keys:", keys)  # noqa: ERA001
            for col_name in self.columns:
                if col_name not in keys:
                    self.columns[col_name]["is_nullable"] = True
            if not isinstance(row, OrderedDict):
                keys = sorted(keys)
            for k in keys:
                v_raw = row[k]
                if not th.is_scalar(v_raw):
                    v = str(v_raw)
                    self.comments[k] = "nested values! example:\n%s" % pprint.pformat(v)
                    logging.warning("in %s: %s" % (k, self.comments[k]))

                # PATCH: Decimals like `"0704.0001"` should be treated as strings, see `nested.json`.
                v_candidate = th.coerce_to_specific(v_raw)
                if isinstance(v_raw, str) and isinstance(v_candidate, Decimal):
                    v = v_raw
                elif isinstance(v_raw, dt.datetime) and isinstance(v_candidate, str):
                    v = v_raw
                else:
                    v = v_candidate

                # print("v_raw, v:", v_raw, v, type(v_raw), type(v))  # noqa: ERA001
                if k not in self.columns:
                    self.columns[k] = {
                        "sample_datum": v,
                        "str_length": len(str(v_raw)),
                        "is_nullable": not (rowcount == 1 and v is not None and str(v).strip()),
                        "is_unique": {
                            v,
                        },
                    }
                else:
                    col = self.columns[k]
                    col["str_length"] = max(col["str_length"], len(str(v_raw)))
                    old_sample_datum = col.get("sample_datum")  # noqa: F841
                    col["sample_datum"] = th.best_representative(col["sample_datum"], v)
                    if (v is None) or (not str(v).strip()):
                        col["is_nullable"] = True
                    if col["is_unique"] is not False:
                        if v in col["is_unique"]:
                            col["is_unique"] = False
                        else:
                            col["is_unique"].add(v)
        for col_name in self.columns:
            col = self.columns[col_name]
            self._fill_metadata_from_sample(col)
            col["is_unique"] = bool(col["is_unique"])
        # print("self.columns:", self.columns)  # noqa: ERA001
