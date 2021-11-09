import re
from typing import Optional, List


def uncapitalize(s: str) -> str:
    return s[0].lower() + s[1:]


def capitalize(s: str) -> str:
    # Note that this implementation differs from str.capitalize() which lowers the remainder of the string
    # I.e. "XXXX".capitalize() == "Xxxx"
    return s[0].upper() + s[1:]


def pluralize(s: str) -> str:
    return s + ("s" if s[-1] != "s" else "")


def indent(s: str, indentation: int = 1) -> str:
    return re.sub(
        "^\\s*$",
        "",
        re.sub("^", " " * 4 * indentation, s, flags=re.MULTILINE),
        flags=re.MULTILINE,
    )


def join_optional(strs: List[Optional[str]], separator: str = "") -> str:
    return separator.join(s for s in strs if s is not None)
