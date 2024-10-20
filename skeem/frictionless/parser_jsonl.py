from frictionless.formats import JsonlParser

read_cell_stream_create_original = JsonlParser.read_cell_stream_create


def read_cell_stream_create(self):
    """
    Patch to frictionless NDJSON reader to not read the whole file.
    """
    cell_stream = read_cell_stream_create_original(self)
    for count, item in enumerate(cell_stream):
        yield item
        if count >= self.resource.detector.sample_size:
            break
