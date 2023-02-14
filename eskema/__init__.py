from eskema import type
from eskema.ddlgen import monkey as ddlgen_monkey
from eskema.frictionless import monkey as frictionless_monkey

ddlgen_monkey.activate()
frictionless_monkey.activate()
type.init()
