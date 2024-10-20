from frictionless.resources import TableResource

from skeem.settings import PEEK_LINES


class TableSampleResource(TableResource):
    """
    Override sample size for frictionless `Resource` instances.
    """

    def __attrs_post_init__(self):
        if self.detector is None:
            from frictionless import Detector

            self.detector = Detector(sample_size=PEEK_LINES)
        super().__attrs_post_init__()
