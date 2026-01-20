import re

def normalize_tool_name(name: str) -> str:
    """
    Convert tool name into a filesystem-safe folder name.
    """
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "-", name)

    return name