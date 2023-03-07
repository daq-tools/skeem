from eskema import type
from eskema.ddlgen import monkey as ddlgen_monkey
from eskema.fastparquet import monkey as fastparquet_monkey
from eskema.frictionless import monkey as frictionless_monkey
from eskema.pandas import monkey as pandas_monkey
from eskema.util.report import get_version

ddlgen_monkey.activate()
frictionless_monkey.activate()
fastparquet_monkey.activate()
pandas_monkey.activate()
type.init()


__appname__ = "eskema"
__version__ = get_version(__appname__)
