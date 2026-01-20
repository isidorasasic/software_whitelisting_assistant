import json
from pathlib import Path
from software_whitelisting_assistant.scripts.classes import Tool, TOC
from pydantic import BaseModel
from typing import Type


TOOLS_DIR = Path(__file__).resolve().parents[1] / "data" /"testing"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)


def save_tool(tool: Tool, toolname: str, base_dir: Path):
    tool_dir = base_dir / toolname
    tool_dir.mkdir(parents=True, exist_ok=True)

    path = tool_dir / f"{toolname}.json"
    path.write_text(tool.model_dump_json(indent=2), encoding="utf-8")


def load_tool(toolname: str) -> Tool:
    path = TOOLS_DIR / toolname / f"{toolname}.json"
    if not path.exists():
        raise FileNotFoundError(f"Tool not found: {path}")
    return Tool.model_validate_json(path.read_text(encoding="utf-8"))


def list_tools() -> list[str]:
    return sorted(p.name for p in TOOLS_DIR.glob("*.json"))


# def toc_path(
#     base_dir: Path,
#     tool_name: str,
#     document_type: str,
# ) -> Path:
#     return (
#         base_dir
#         / tool_name
#         / f"toc_{document_type.lower().replace(' ', '_')}.json"
#     )


def save_toc(toc: TOC, toolname: str) -> None:
    path = TOOLS_DIR / toolname / f"toc_{toolname}.json"
    path.write_text(toc.model_dump_json(indent=2), encoding="utf-8")


def load_toc(toolname: str) -> TOC:
    path = TOOLS_DIR / toolname / f"toc_{toolname}.json"
    return TOC.model_validate_json(path.read_text(encoding="utf-8"))


def toc_exists(path: Path) -> bool:
    return path.exists()