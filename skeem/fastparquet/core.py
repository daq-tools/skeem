import fastparquet.cencoding as encoding
import numpy as np
import pandas as pd
from fastparquet import parquet_thrift
from fastparquet.cencoding import ThriftObject
from fastparquet.converted_types import convert
from fastparquet.core import read_data_page, read_data_page_v2, read_dictionary_page

from skeem.settings import PEEK_LINES


def read_col(column, schema_helper, infile, use_cat=False, selfmade=False, assign=None, catdef=None, row_filter=None):
    """Using the given metadata, read one column in one row-group.

    Parameters
    ----------
    column: thrift structure
        Details on the column
    schema_helper: schema.SchemaHelper
        Based on the schema for this parquet data
    infile: open file or string
        If a string, will open; if an open object, will use as-is
    use_cat: bool (False)
        If this column is encoded throughout with dict encoding, give back
        a pandas categorical column; otherwise, decode to values
    row_filter: bool array or None
        if given, selects which of the values read are to be written
        into the output. Effectively implies NULLs, even for a required
        column.
    """
    cmd = column.meta_data
    se = schema_helper.schema_element(cmd.path_in_schema)
    off = min((cmd.dictionary_page_offset or cmd.data_page_offset, cmd.data_page_offset))
    infile.seek(off)
    column_binary = infile.read(cmd.total_compressed_size)
    infile = encoding.NumpyIO(column_binary)
    rows = row_filter.sum() if isinstance(row_filter, np.ndarray) else cmd.num_values

    if use_cat:
        my_nan = -1
    else:
        if assign.dtype.kind in ["i", "u", "b"]:
            my_nan = pd.NA
        elif assign.dtype.kind == "f":
            my_nan = np.nan
        elif assign.dtype.kind in ["M", "m"]:
            # GH#489 use a NaT representation compatible with ExtensionArray
            my_nan = assign.dtype.type("NaT")
        else:
            my_nan = None

    num = 0  # how far through the output we are
    row_idx = [0]  # map/list objects
    dic = None
    index_off = 0  # how far through row_filter we are

    while num < rows:
        off = infile.tell()
        ph = ThriftObject.from_buffer(infile, "PageHeader")
        if ph.type == parquet_thrift.PageType.DICTIONARY_PAGE:
            dic2 = read_dictionary_page(infile, schema_helper, ph, cmd, utf=se.converted_type == 0)
            dic2 = convert(dic2, se)
            if use_cat and dic is not None and (dic2 != dic).any():
                raise RuntimeError("Attempt to read as categorical a column" "with multiple dictionary pages.")
            dic = dic2
            if use_cat and dic is not None:
                # fastpath skips the check the number of categories hasn't changed.
                # In this case, they may change, if the default RangeIndex was used.
                ddt = [kv.value.decode() for kv in (cmd.key_value_metadata or []) if kv.key == b"label_dtype"]
                ddt = ddt[0] if ddt else None
                catdef._set_categories(pd.Index(dic, dtype=ddt), fastpath=True)
                if np.iinfo(assign.dtype).max < len(dic):
                    raise RuntimeError(
                        "Assigned array dtype (%s) cannot accommodate "
                        "number of category labels (%i)" % (assign.dtype, len(dic))
                    )
            continue
        if ph.type == parquet_thrift.PageType.DATA_PAGE_V2:
            num += read_data_page_v2(
                infile,
                schema_helper,
                se,
                ph.data_page_header_v2,
                cmd,
                dic,
                assign,
                num,
                use_cat,
                off,
                ph,
                row_idx,
                selfmade=selfmade,
                row_filter=row_filter,
            )
            continue
        if selfmade and hasattr(cmd, "statistics") and getattr(cmd.statistics, "null_count", 1) == 0:
            skip_nulls = True
        else:
            skip_nulls = False
        defi, rep, val = read_data_page(infile, schema_helper, ph, cmd, skip_nulls, selfmade=selfmade)
        max_defi = schema_helper.max_definition_level(cmd.path_in_schema)
        if isinstance(row_filter, np.ndarray):
            io = index_off + len(val)  # will be new index_off
            if row_filter[index_off : index_off + len(val)].sum() == 0:
                num += len(defi) if defi is not None else len(val)
                continue
            if defi is not None:
                val = val[row_filter[index_off : index_off + len(defi)][defi == max_defi]]
                defi = defi[row_filter[index_off : index_off + len(defi)]]
            else:
                val = val[row_filter[index_off : index_off + len(val)]]
            rep = rep[row_filter[index_off : index_off + len(defi)]] if rep is not None else rep
            index_off = io
        if rep is not None and assign.dtype.kind != "O":  # pragma: no cover
            # this should never get called
            raise ValueError(
                "Column contains repeated value, must use object " "type, but has assumed type: %s" % assign.dtype
            )
        d = ph.data_page_header.encoding in [
            parquet_thrift.Encoding.PLAIN_DICTIONARY,
            parquet_thrift.Encoding.RLE_DICTIONARY,
        ]
        if use_cat and not d:
            if not hasattr(catdef, "_set_categories"):
                raise ValueError(
                    "Returning category type requires all chunks" " to use dictionary encoding; column: %s",
                    cmd.path_in_schema,
                )

        if rep is not None:
            null = not schema_helper.is_required(cmd.path_in_schema[0])
            null_val = se.repetition_type != parquet_thrift.FieldRepetitionType.REQUIRED
            row_idx[0] = 1 + encoding._assemble_objects(
                assign, defi, rep, val, dic, d, null, null_val, max_defi, row_idx[0]
            )
        elif defi is not None:
            part = assign[num : num + len(defi)]
            if isinstance(part.dtype, pd.core.arrays.masked.BaseMaskedDtype):
                # TODO: could have read directly into array
                part._mask[:] = defi != max_defi
                part = part._data
            elif part.dtype.kind != "O":
                part[defi != max_defi] = my_nan
            if d and not use_cat:
                part[defi == max_defi] = dic[val]
            elif not use_cat:
                part[defi == max_defi] = convert(val, se)
            else:
                part[defi == max_defi] = val
        else:
            piece = assign[num : num + len(val)]
            if isinstance(piece.dtype, pd.core.arrays.masked.BaseMaskedDtype):
                piece = piece._data
            if use_cat and not d:
                # only possible for multi-index
                val = convert(val, se)
                try:
                    i = pd.Categorical(val)
                except:
                    i = pd.Categorical(val.tolist())
                catdef._set_categories(pd.Index(i.categories), fastpath=True)
                piece[:] = i.codes
            elif d and not use_cat:
                piece[:] = dic[val]
            elif not use_cat:
                piece[:] = convert(val, se)
            else:
                piece[:] = val

        num += len(defi) if defi is not None else len(val)

        # PATCH for Skeem: Terminate `read_col` early, in order to not load the whole file.
        if num >= PEEK_LINES:
            break
