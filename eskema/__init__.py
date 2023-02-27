from eskema import type
from eskema.ddlgen import monkey as ddlgen_monkey
from eskema.fastparquet import monkey as fastparquet_monkey
from eskema.frictionless import monkey as frictionless_monkey
from eskema.pandas import monkey as pandas_monkey

ddlgen_monkey.activate()
frictionless_monkey.activate()
fastparquet_monkey.activate()
pandas_monkey.activate()
type.init()
