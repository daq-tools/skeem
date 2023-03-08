def read_byte_stream_create(self):
    """
    Don't croak when reading streams without `name` attribute.
    """
    from frictionless import FrictionlessException, errors
    from frictionless.schemes.stream.loader import ReusableByteStream

    byte_stream = self.resource.data
    # TODO: Submit patch to upstream.
    # PATCH for Skeem: Enable reading from nameless streams.
    """
    if not os.path.isfile(byte_stream.name):  # type: ignore
        note = f"only local streams are supported: {byte_stream}"
        raise FrictionlessException(errors.SchemeError(note=note))
    """
    if hasattr(byte_stream, "encoding"):
        try:
            byte_stream = open(byte_stream.name, "rb")  # type: ignore
        except Exception:
            note = f"cannot open a stream in the byte mode: {byte_stream}"
            raise FrictionlessException(errors.SchemeError(note=note))  # noqa: B904
    byte_stream = ReusableByteStream(byte_stream)
    return byte_stream
