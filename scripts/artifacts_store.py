import json
from pathlib import Path
from datetime import datetime
from typing import List
from software_whitelisting_assistant.scripts.classes import Tool, TOC, InjectedIssue
from software_whitelisting_assistant.scripts.utils import normalize_name


TOOLS_DIR = Path(__file__).resolve().parents[1] / "data"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# prompt path
PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

def load_prompt(name: str) -> str:
    """
    Load a prompt template from disk.

    Args:
        name (str): The filename of the prompt template to load, relative to PROMPTS_DIR.

    Returns:
        str: The contents of the prompt file as a UTF-8 string.

    Raises:
        FileNotFoundError: If the prompt file does not exist at the expected path.
    """
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def save_tool(tool: Tool, tool_dir: Path):
    """
    Save a Tool object to disk as a JSON file.

    Args:
        tool (Tool): The Tool object to serialize and save.
        tool_dir (Path): Directory where the TOC file will be written.
    """

    path = tool_dir / f"{normalize_name(tool.name)}.json"
    path.write_text(tool.model_dump_json(indent=2), encoding="utf-8")


def load_tool(toolname: str) -> Tool:
    """
    Load a Tool json object from disk.

    Args:
        toolname (str): The name of the tool to load.

    Returns:
        Tool: The loaded and validated Tool object.

    Raises:
        FileNotFoundError: If the tool JSON file does not exist.
    """
    path = TOOLS_DIR / toolname / f"{toolname}.json"
    if not path.exists():
        raise FileNotFoundError(f"Tool not found: {path}")
    return Tool.model_validate_json(path.read_text(encoding="utf-8"))


def save_toc(toc: TOC, tool_dir, toc_name: str):
    """
    Save a table of contents (TOC) to disk as a JSON file.

    Args:
        toc (TOC): The table of contents to serialize and save.
        tool_dir (Path): Directory where the TOC file will be written.
        toc_name (str): Name of the TOC file (without extension).
    """
    path = tool_dir / f"{toc_name}.json"
    path.write_text(toc.model_dump_json(indent=2), encoding="utf-8")


def load_toc(toolname, document_name: str) -> TOC:
    """
    Load a table of contents (TOC) for a tool from disk.

    Args:
        toolname (str): The name of the tool whose TOC should be loaded.
        document_name ( str): The normalized name of the document type (e.g. terms_of_service)

    Returns:
        TOC: The loaded and validated TOC object.
    """
    path = TOOLS_DIR / toolname / f"toc_{document_name}.json"
    return TOC.model_validate_json(path.read_text(encoding="utf-8"))


def save_html(
    html: str,
    tool_dir: Path,
    document_name: str
):
    """
    Save a full HTML document to disk.

    Args:
        html (str): The full HTML content to save.
        tool_dir (Path): Directory where the HTML file will be written.
        document_name (str): Base name of the document (without extension).
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
    temperature_section: float,
    max_tokens_tool: int,
    max_tokens_toc: int,
    max_tokens_section: int,
    issue_sections: List[InjectedIssue]
) -> Path:
    """
    Save metadata describing a generated document and its generation parameters.

    Args:
        tool (Tool): The tool for which the document was generated.
        toc (TOC): The table of contents associated with the document.
        document_type (str): The type of the generated document.
        tool_dir (Path): Directory where the metadata file will be saved.
        model_tool (str): Model used for tool generation.
        model_toc (str): Model used for TOC generation.
        model_section (str): Model used for section content generation.
        temperature_tool (float): Sampling temperature for tool generation.
        temperature_section (float): Sampling temperature for section generation.
        max_tokens_tool (int): Token limit for tool generation.
        max_tokens_toc (int): Token limit for TOC generation.
        max_tokens_section (int): Token limit for section generation.
        issue_sections (List[InjectedIssue]): List of injected issues found in the
            generated document.

    Returns:
        Path: The path to the saved metadata JSON file.
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

    filename = normalize_name(document_type)
    metadata_path = tool_dir / f"{filename}_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return metadata_path
