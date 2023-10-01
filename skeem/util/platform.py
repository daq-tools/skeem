import platform

from skeem.util.report import bullet_item, subsection


def about_platform():
    subsection("Python")
    print(bullet_item(platform.platform()))
    print()

    # SQLAlchemy
    from importlib.metadata import entry_points

    import sqlalchemy.dialects

    subsection("SQLAlchemy")
    print(bullet_item(sqlalchemy.dialects.registry.impls.keys(), label="Dialects built-in"))
    eps = entry_points(group="sqlalchemy.dialects")
    dialects = [dialect.name for dialect in eps]
    print(bullet_item(dialects, label="Dialects 3rd-party"))
    print(bullet_item(sqlalchemy.dialects.plugins.impls.keys(), label="Plugins"))
    print()

    # fsspec
    import fsspec

    subsection("fsspec protocols")
    print(bullet_item(fsspec.available_protocols()))
    print()

    subsection("fsspec compressions")
    print(bullet_item(fsspec.available_compressions()))
    print()

    # pandas
    subsection("pandas module versions")
    import pandas

    pandas.show_versions(as_json=False)
    print()
