import json
from pathlib import Path
from datetime import datetime
from typing import List
from software_whitelisting_assistant.scripts.classes import Tool, TOC, InjectedIssue


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


def save_tool_context(
    tool_dir: Path,
    tool_name: str,
    document_types: list[str],
):
    path = tool_dir / "context.json"
    payload = {
        "tool_name": tool_name,
        "document_types": document_types,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_toc(toc: TOC, tool_dir, toc_name: str):
    path = tool_dir / f"{toc_name}.json"
    path.write_text(toc.model_dump_json(indent=2), encoding="utf-8")


def load_toc(toolname: str) -> TOC:
    path = TOOLS_DIR / toolname / f"toc_{toolname}.json"
    return TOC.model_validate_json(path.read_text(encoding="utf-8"))


def toc_exists(path: Path) -> bool:
    return path.exists()


def save_html(
    html: str,
    tool_dir: Path,
    document_name: str
):
    """
    Saves a full HTML document.
    Returns the saved path.
    """

    document_name = document_name.replace("-", "_")
    path = tool_dir / f"{document_name}.html"
    path.write_text(html, encoding="utf-8")


def save_metadata(
    *,
    tool: Tool,
    toc: TOC,
    document_type: str,
    tool_dir: Path,
    model_tool: str,
    model_toc: str,
    model_section: str,
    temperature_tool: float,
    temperature_toc: float,
    temperature_section: float,
    max_tokens_tool: int,
    max_tokens_toc: int,
    max_tokens_section: int,
    issue_sections: List[InjectedIssue]
) -> Path:
    """
    Save metadata for a single generated document.
    Returns the path to the metadata JSON file.
    """

    titles_with_issues = [issue.section_title for issue in issue_sections]

    metadata = {
        "tool": {
            "name": tool.name,
            "purpose": tool.purpose,
            "category": tool.category,
            "user_base": tool.user_base
        },
        "document": {
            "id": toc.id,
            "title": toc.title,
            "type": document_type
        },
        "generation": {
            "model_tool": model_tool,
            "model_toc": model_toc,
            "model_section": model_section,
            "temperature_tool": temperature_tool,
            "temperature_toc": temperature_toc,
            "temperature_section": temperature_section,
            "max_tokens_tool": max_tokens_tool,
            "max_tokens_toc": max_tokens_toc,
            "max_tokens_section": max_tokens_section
        },
        "issues": {
            "total_count": len(titles_with_issues),
            "sections_with_issues": titles_with_issues
        },
        "timestamp": datetime.now().isoformat()
    }

    filename = toc.id.replace("-", "_")
    metadata_path = tool_dir / f"{filename}_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return metadata_path
