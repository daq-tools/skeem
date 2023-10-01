import ddlgenerator.ddlgenerator
import ddlgenerator.reshape
import ddlgenerator.typehelpers

from .ddlgenerator import AnyDialect, TablePlus
from .reshape import clean_key_name, use_this_pk
from .typehelpers import best_coercable, coerce_to_specific


def activate():
    ddlgenerator.ddlgenerator.mock_engines = AnyDialect()
    ddlgenerator.ddlgenerator.Table = TablePlus
    ddlgenerator.reshape.clean_key_name = clean_key_name
    ddlgenerator.reshape.ParentTable.use_this_pk = use_this_pk
    ddlgenerator.typehelpers.best_coercable = best_coercable
    ddlgenerator.typehelpers.coerce_to_specific = coerce_to_specific
