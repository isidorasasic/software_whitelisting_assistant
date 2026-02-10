import re
from software_whitelisting_assistant.scripts.classes import InjectedIssue


def normalize_name(name: str) -> str:
    """
    Convert a string into a filesystem-safe folder or file name.

    Args:
        name (str): The original name string to normalize.

    Returns:
        str: A normalized, filesystem-safe string.
    """
    name = name.lower().strip()
    name = name.replace("&", "and")
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "_", name)

    return name


def print_injected_issues(
    issue: InjectedIssue,
    level: int
):
    """
    Print injected issue to the console with formatting and indentation.

    Args:
        issue (InjectedIssue): Injected issue to print.
        level (int): The nesting level of the parent section.
    """
    if not issue:
        return

    indent = "  " * (level - 1)
    print(f"{indent}⚠️  Injected issue:")

    sev = f" [{issue.severity}]" if issue.severity else ""
    print(f"{issue.description}{sev}")


def print_section_console(
    title: str,
    content: str,
    level: int,
    parent_title: str | None
):
    """
    Print a formatted section to the console with indentation based on its level.

    Args:
        title (str): The title of the section.
        content (str): The text content of the section.
        level (int): The nesting level of the section (used to determine indentation).
        parent_title (str | None): The title of the parent section, if any.
    """
    indent = "  " * (level - 1)

    if parent_title:
        print(f"\n{indent}{parent_title} → {title}")
    else:
        print(f"\n{indent}{title}")

    print(f"{indent}{'-' * 60}")

    for line in content.splitlines():
        print(f"{indent}{line}")

    print()