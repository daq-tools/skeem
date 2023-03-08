from frictionless import Resource

from skeem.settings import PEEK_LINES


class ResourcePlus(Resource):
    """
    Override sample size for frictionless `Resource` instances.
    """

    def __init__(self, *args, **kwargs):
        from frictionless import Detector

        if "detector" not in kwargs:
            kwargs["detector"] = Detector(sample_size=PEEK_LINES)
        super().__init__(*args, **kwargs)
