import ast
import io
import logging
import typing as t
from copy import deepcopy

import pandas as pd
import sqlalchemy
from cachetools.func import lru_cache
from data_dispenser import Source

from skeem.io import dataframe_from_lineprotocol, dataset_to_dataframe, to_tempfile
from skeem.settings import PEEK_LINES

logger = logging.getLogger(__name__)

try:
    from pymongo.collection import Collection as MongoCollection
except ImportError:  # pragma: no cover
    logger.info("Could not import Collection from pymongo; is it installed?")

    class MongoCollection:  # type: ignore[no-redef]
        pass


class SourcePlus(Source):
    def __init__(
        self,
        src: t.Any,
        limit: int = None,
        fieldnames: t.List[str] = None,
        table: t.Optional[str] = None,
        ext: t.Optional[str] = None,
    ):
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
        self.deserializers: t.List[t.Callable] = []
        self.table_name = "Table%d" % (SourcePlus.table_count)
        self.fieldnames = fieldnames
        self.db_engine = None
        SourcePlus.table_count += 1

        self.src = src
        self.table = table
        self.ext = ext

        self.autodetect()

    def autodetect(self):
        """
        Dispatch input data by its type to the corresponding handler function.
        """
        src = self.src
        table = self.table
        ext = self.ext
        if isinstance(src, sqlalchemy.sql.schema.MetaData):
            self._source_is_sqlalchemy_metadata(src, table or "*")
            return
        if isinstance(src, MongoCollection):
            self._source_is_mongo(src)
            return
        if hasattr(src, "startswith") and (src.startswith("http://") or src.startswith("https://")):
            self._source_is_url(src)
            return
        if hasattr(src, "read"):  # open file or buffer
            if ext in [".xlsx", ".ods"]:
                self._source_is_excel(src, sheet=table or 0)
            else:
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
        """
        Register improved content type handler functions for certain data formats.
        """
        self.eval_funcs_by_ext[".csv"] = [_eval_csv]
        self.eval_funcs_by_ext[".grib2"] = [_eval_grib2]
        self.eval_funcs_by_ext[".lp"] = [_eval_lineprotocol]
        self.eval_funcs_by_ext[".nc"] = [_eval_netcdf]
        self.eval_funcs_by_ext[".ndjson"] = [_eval_ndjson]

        # TODO: Use the generic interface if deserializer can be created with `sheet_name` option.

    def _source_is_readable(self, src, ext="*"):
        """
        A generic deserializer function for reading open files or buffers.
        """
        if hasattr(src, "name"):
            self.table_name = src.name
        deserializers = self.eval_funcs_by_ext.get(ext or "*")
        if deserializers is None:
            raise NotImplementedError(f"Backend 'ddlgen' has no deserializer for extension '{ext}'")
        self.deserializers = deserializers
        self._deserialize(src)

    def _source_is_excel(self, spreadsheet, sheet=None):
        df = pd.read_excel(spreadsheet, sheet_name=sheet, parse_dates=False, keep_default_na=False, nrows=PEEK_LINES)
        self.generator = _generate_records(df)


def _eval_csv(target, fieldnames: t.List[str] = None, *args, **kwargs):
    """
    Generate records from a CSV string, using pandas' `pd.read_csv`.
    """
    df = pd.read_csv(target, parse_dates=False, keep_default_na=False, nrows=PEEK_LINES)
    return _generate_records(df)


def _eval_lineprotocol(target, fieldnames: t.List[str] = None, *args, **kwargs):
    """
    Generate records from an InfluxData lineprotocol string.
    """
    df = dataframe_from_lineprotocol(data=target)
    return _generate_records(df)


# Work around being called twice.
# TODO: Find the root cause why those functions are called twice.
@lru_cache  # type: ignore[arg-type]
def _eval_grib2(target, fieldnames: t.List[str] = None, *args, **kwargs):
    """
    Generate records from an NDJSON string, using pandas' `pd.read_json`.
    """
    import cfgrib
    import xarray as xr

    tmp = to_tempfile(target)
    gribfile = tmp.name

    """
    # WARNING: Falling back to 'lalala'. Reason: multiple values for unique key,
    # try re-open the file with one of ...

    # CMC_geps-raw_SPFH_TGL_40_latlon0p5x0p5_2023022512_P000_allmbrs.grib2
    #     filter_by_keys={'dataType': 'cf'}
    #     filter_by_keys={'dataType': 'pf'}

    # CMC_HRDPA_APCP-006-0100cutoff_SFC_0_ps2.5km_2023012606_000.grib2
    #     filter_by_keys={'stepType': 'accum'}
    #     filter_by_keys={'stepType': 'avg'}
    """
    logger.info("Opening dataset")
    try:
        ds = xr.open_dataset(gribfile, engine="cfgrib")
    except cfgrib.dataset.DatasetBuildError as ex:
        msg = str(ex)
        if "multiple values for unique key" in msg:
            candidates = msg.splitlines()[1:]
            candidate = candidates[0].strip()
            logger.info(f"WARNING: Falling back to '{candidate}'. Reason: {ex}")
            kwargs = ast.literal_eval(f"dict({candidate})")
            ds = xr.open_dataset(gribfile, engine="cfgrib", **kwargs, decode_times=False)
        else:
            raise
    df = dataset_to_dataframe(ds, peek_lines=PEEK_LINES)
    return _generate_records(df)


# Work around being called twice.
# TODO: Find the root cause why those functions are called twice.
@lru_cache  # type: ignore[arg-type]
def _eval_netcdf(target, fieldnames: t.List[str] = None, *args, **kwargs):
    """
    Generate records from an NDJSON string, using pandas' `pd.read_json`.
    """
    import xarray as xr

    # FIXME: Because this function is called two times, we need to copy the
    #        buffer, because `xr.open_dataset` will apparently close it.
    target = deepcopy(target)

    logger.info("Opening dataset")
    ds = xr.open_dataset(target, engine="scipy")
    df = dataset_to_dataframe(ds, peek_lines=PEEK_LINES)
    return _generate_records(df)


def _eval_ndjson(target, fieldnames: t.List[str] = None, *args, **kwargs):
    """
    Generate records from an NDJSON string, using pandas' `pd.read_json`.
    """
    df = pd.read_json(target, convert_dates=False, lines=True, nrows=PEEK_LINES)
    return _generate_records(df)


def _generate_records(df: pd.DataFrame):
    """
    Generate individual dict-type records from pandas dataframe.
    """
    for record in df.to_dict(orient="records"):
        yield record
