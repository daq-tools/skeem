import textwrap
import typing as t

from colorama import Fore, Style

string_or_list = t.Union[str, t.List[str]]


def section(text: str):
    return armor(text, title)


def subsection(text: str):
    return armor(text, subtitle)


def armor(text: str, formatter: t.Callable):
    guard = "=" * len(text)
    print(guard)
    print(formatter(text))
    print(guard)


def title(text: str):
    return Fore.CYAN + Style.BRIGHT + text + Style.RESET_ALL


def subtitle(text: str):
    return Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL


def text_list(data: string_or_list):
    if isinstance(data, str):
        return data
    elif isinstance(data, t.List):
        return ", ".join(data)
    else:
        raise ValueError("Unable to flatten list")


def bullet_list(data: t.List[str]):
    data.sort()
    lines = [f"- {text_list(line)}" for line in data]
    return "\n".join(lines)


def wrap_list(data: t.List[str], **kwargs):
    data = [item for item in data if item is not None]
    data.sort()
    text = ", ".join(data)
    return "\n".join(textwrap.wrap(text, width=80, **kwargs))


def bullet_item(data: string_or_list, label: str = None):
    if data is None:
        return None
    if label is None:
        label = ""
    else:
        label = f"{label}: "
    if isinstance(data, (t.List, t.KeysView, t.ValuesView)):
        text = wrap_list(list(data), subsequent_indent="  ")
    else:
        text = data
    return f"- {label}{text}"


def get_version(appname):
    from importlib.metadata import PackageNotFoundError, version  # noqa

    try:
        return version(appname)
    except PackageNotFoundError:  # pragma: no cover
        return "unknown"
