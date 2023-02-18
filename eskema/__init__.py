from eskema import type
from eskema.ddlgen import monkey as ddlgen_monkey
from eskema.frictionless import monkey as frictionless_monkey
from eskema.fsspec import monkey as fsspec_monkey

ddlgen_monkey.activate()
frictionless_monkey.activate()
fsspec_monkey.activate()
type.init()
