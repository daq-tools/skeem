import logging

logger = logging.getLogger(__name__)


def create_parser(self, resource):
    """
    Apply sample size to pandas parser as well.
    """
    from frictionless.formats import PandasParser

    if resource.format == "pandas":
        # TODO: Submit patch to upstream.
        # PATCH for Skeem: Speed up inference by not loading the whole file.
        logger.info(f"Loading data using sample_size={resource.detector.sample_size}")
        resource.data = resource.data.head(resource.detector.sample_size)
        logger.info(f"Data loaded with size={len(resource.data)}")  # noqa: ERA001
        return PandasParser(resource)

    return None
