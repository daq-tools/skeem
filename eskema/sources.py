import io
import logging

import pandas as pd
import sqlalchemy
from data_dispenser import Source

logger = logging.getLogger(__name__)

try:
    from pymongo.collection import Collection as MongoCollection
except ImportError:
    logger.info("Could not import Collection from pymongo; is it installed?")

    class MongoCollection:  # type: ignore[no-redef]
        pass


# How many lines to read from input data.
PEEK_LINES = 1000


class SourcePlus(Source):
    def __init__(self, src, limit=None, fieldnames=None, table="*", ext=None):
        """
        For ``.csv`` and ``.xls``, field names will be taken from
        the first line of data found - unless ``fieldnames`` is given,
        in which case, it will override.  For ``.xls``, ``fieldnames``
        may be an integer, in which case it will be the (1-based) row number
        field names will be taken from (rows before that will be discarded).
        """
        self.improve()

        self.counter = 0
        self.limit = limit
        self.deserializers = []
        self.table_name = "Table%d" % (SourcePlus.table_count)
        self.fieldnames = fieldnames
        self.db_engine = None
        SourcePlus.table_count += 1

        self.src = src
        self.table = table
        self.ext = ext

        self.autodetect()

    def autodetect(self):
        src = self.src
        table = self.table
        ext = self.ext
        if isinstance(src, sqlalchemy.sql.schema.MetaData):
            self._source_is_sqlalchemy_metadata(src, table)
            return
        if isinstance(src, MongoCollection):
            self._source_is_mongo(src)
            return
        if hasattr(src, "startswith") and (src.startswith("http://") or src.startswith("https://")):
            self._source_is_url(src)
            return
        if hasattr(src, "read"):  # open file or buffer
            self._source_is_readable(src, ext=ext)
            return
        if hasattr(src, "__next__"):
            self._source_is_generator(src)
            return

        # Don't allow filesystem access on un-sanitized input data.
        """
        if os.path.isfile(src):
            if src.endswith(".xls"):
                self._source_is_excel(src, sheet=table)
            else:
                self._source_is_path(src)
            return
        """

        # Don't allow `eval` on un-sanitized input data.
        """
        try:
            data = eval(src)
            if not hasattr(data, "__next__"):
                data = iter(data)
            self._source_is_generator(data)
            return
        except:
            pass
        """

        # Don't allow filesystem access on un-sanitized input data.
        """
        # Try to interpret source as filesystem glob pattern.
        try:
            sources = sorted(glob.glob(src))
            if sources:
                self._multiple_sources(sources)
                return
        except TypeError:
            pass
        """

        # Try to interpret source as text string.
        if isinstance(src, str):
            buffer = io.StringIO(src.strip())
            self._source_is_readable(buffer, ext=ext)
            return

        raise NotImplementedError("Could not read data source %s of type %s" % (str(src), str(type(src))))

    def improve(self):
        self.eval_funcs_by_ext[".csv"] = [_eval_csv]
        self.eval_funcs_by_ext[".ndjson"] = [_eval_ndjson]

    def _source_is_readable(self, src, ext="*"):
        if hasattr(src, "name"):
            self.table_name = src.name
        self.deserializers = self.eval_funcs_by_ext.get(ext or "*")
        self._deserialize(src)


def _eval_csv(target, fieldnames=None, *args, **kwargs):
    """
    Generate records from a CSV string, using pandas' `pd.read_csv`.
    """
    df = pd.read_csv(target, parse_dates=False, keep_default_na=False, nrows=PEEK_LINES)
    return _generate_records(df)


def _eval_ndjson(target, fieldnames=None, *args, **kwargs):
    """
    Generate records from an NDJSON string, using pandas' `pd.read_json`.
    """
    df = pd.read_json(target, convert_dates=False, lines=True, nrows=PEEK_LINES)
    return _generate_records(df)


def _generate_records(df):
    for record in df.to_dict(orient="records"):
        yield record
