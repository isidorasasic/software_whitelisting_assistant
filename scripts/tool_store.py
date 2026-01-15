import json
from pathlib import Path
from classes import Tool

TOOLS_DIR = Path(__file__).resolve().parents[1] / "data" / "tools"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)


def save_tool(tool: Tool, filename: str) -> None:
    path = TOOLS_DIR / filename
    path.write_text(tool.model_dump_json(indent=2), encoding="utf-8")


def load_tool(filename: str) -> Tool:
    path = TOOLS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Tool not found: {path}")
    return Tool.model_validate_json(path.read_text(encoding="utf-8"))


def list_tools() -> list[str]:
    return sorted(p.name for p in TOOLS_DIR.glob("*.json"))
