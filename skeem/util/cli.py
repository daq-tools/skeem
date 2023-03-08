import logging
import sys
import textwrap
import typing as t

import click

logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    """
    Setup loggers.
    """

    # Define log format.
    log_format = "%(asctime)-15s [%(name)-34s] %(levelname)-7s: %(message)s"

    # Because `ddlgenerator` already invokes `logging.basicConfig()`, we need to apply `force`.
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level, force=True)


def boot_click(ctx: click.Context, verbose: bool = False, debug: bool = False, trace_modules: t.List[str] = None):
    """
    Bootstrap the CLI application.
    """
    trace_modules = trace_modules or []

    # Adjust log level according to `verbose` / `debug` flags.
    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Setup logging, according to `verbose` / `debug` flags.
    setup_logging(level=log_level)

    # Enable `ddlgenerator` logger only with `--debug`.
    if not debug:
        root_logger = logging.getLogger("root")  # noqa: ERA001
        root_logger.disabled = True  # noqa: ERA001

    # Optionally enable code tracing.
    if trace_modules:
        enable_tracing(modules=to_list(trace_modules))


def split_list(value: str, delimiter: str = ",") -> t.List[str]:
    if value is None:
        return []
    return [c.strip() for c in value.split(delimiter)]


def to_list(x: t.Any, default: t.List[t.Any] = None) -> t.List[t.Any]:
    if not isinstance(default, t.List):
        raise ValueError("Default value is not a list")
    if x is None:
        return default
    if not isinstance(x, t.Iterable) or isinstance(x, str):
        return [x]
    elif isinstance(x, list):
        return x
    else:
        return list(x)


def enable_tracing(modules: t.List[str]):
    effective_modules = []
    for module in modules:
        if module == "machinery":
            effective_modules += ["skeem", "fastparquet", "frictionless", "fsspec", "pandas"]
        if module == "core":
            effective_modules += ["skeem"]
        else:
            effective_modules += [module]
    try:
        import hunter  # noqa: F401

        _enable_tracing(sorted(set(effective_modules)))
    except ImportError:
        logger.warning("Package `hunter` not installed")


def _enable_tracing(modules: t.List[str] = None):
    from hunter import Q, trace

    if not modules:
        return

    logger.info(f"Tracing modules {modules}")
    constraint = Q(module_startswith=modules[0])
    for module in modules[1:]:
        constraint = constraint | Q(module_startswith=module)
    trace(constraint)


def docstring_format_verbatim(text: t.Optional[str]) -> str:
    """
    Format docstring to be displayed verbatim as a help text by Click.

    - https://click.palletsprojects.com/en/8.1.x/documentation/#preventing-rewrapping
    - https://github.com/pallets/click/issues/56
    """
    text = text or ""
    text = textwrap.dedent(text)
    lines = [line if line.strip() else "\b" for line in text.splitlines()]
    return "\n".join(lines)
