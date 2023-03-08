from urllib.parse import urlparse

from botocore import UNSIGNED
from botocore.client import Config
from frictionless import platform
from frictionless.schemes import AwsControl
from frictionless.schemes.aws.loaders.s3 import S3ByteStream


def read_byte_stream_create(self):
    """
    Patched version to allow anonymous access to public S3 buckets.

    TODO: Maybe apply only conditionally?

    https://stackoverflow.com/a/34866092
    """
    control = AwsControl.from_dialect(self.resource.dialect)
    parts = urlparse(self.resource.normpath, allow_fragments=False)

    # PATCH for Skeem: Allow anonymous access to public S3 buckets.
    config = Config(signature_version=UNSIGNED)
    client = platform.boto3.resource("s3", endpoint_url=control.s3_endpoint_url, config=config)

    object = client.Object(bucket_name=parts.netloc, key=parts.path[1:])  # type: ignore  # noqa: A001
    byte_stream = S3ByteStream(object)
    return byte_stream
