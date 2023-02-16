import logging

logger = logging.getLogger(__name__)


def create_parser(self, resource):
    """
    Apply sample size to pandas parser as well.
    """
    from frictionless.formats import PandasParser

    if resource.format == "pandas":
        # TODO: Submit patch to upstream.
        # PATCH for Eskema to speed up inference by not loading the whole file.
        logger.info(f"Using sample size: {resource.detector.sample_size}")
        resource.data = resource.data.head(resource.detector.sample_size)
        return PandasParser(resource)

    return None
