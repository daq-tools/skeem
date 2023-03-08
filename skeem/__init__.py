from skeem import type
from skeem.ddlgen import monkey as ddlgen_monkey
from skeem.fastparquet import monkey as fastparquet_monkey
from skeem.frictionless import monkey as frictionless_monkey
from skeem.pandas import monkey as pandas_monkey
from skeem.util.report import get_version

ddlgen_monkey.activate()
frictionless_monkey.activate()
fastparquet_monkey.activate()
pandas_monkey.activate()
type.init()


__appname__ = "skeem"
__version__ = get_version(__appname__)
