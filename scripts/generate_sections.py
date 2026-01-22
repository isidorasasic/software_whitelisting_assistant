from typing import List, Set, Tuple
from software_whitelisting_assistant.scripts.classes import Tool, TOC, TOCSection, Section, SectionLLMOutput, InjectedIssue
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt
from software_whitelisting_assistant.scripts import load_config
import random
import json
from bs4 import BeautifulSoup


def summarize_previous_sections(sections, limit: int = 3) -> str:
    """
    Provide lightweight context for continuity without token bloat.
    Args:
        sections (Section): Sections to be summarized.
        limit (int): Number of sections for summarization.
    """
    if not sections:
        return "None"

    recent = sections[-limit:]
    return "\n".join(f"- {s.title}" for s in recent)


def save_issue_metadata(path, issue_sections: set[str]):
    """
    Save metadata about sections that have issues to a JSON file.

    Args:
        path (Path): The file path where the metadata JSON will be saved.
        issue_sections (set[str]): A set of section IDs that have issues.
    """

    path.write_text(
        json.dumps(
            {
                "sections_with_issues": sorted(issue_sections)
            },
            indent=2
        ),
        encoding="utf-8",
    )


def collect_section_ids(toc) -> list[str]:
    """
    Collect all section IDs from a table of contents (TOC) recursively.

    Args:
        toc: An object representing the table of contents.

    Returns:
        list[str]: A list of all section IDs in the TOC, in depth-first order.
    """
    ids: list[str] = []

    def walk(section):
        ids.append(section.id)
        for child in section.subsections:
            walk(child)

    for top in toc.sections:
        walk(top)

    return ids


def get_issue_sections(
    section_ids: list[str],
    min_issues: int,
    max_issues: int,
) -> Set[str]:
    """
    Randomly select section IDs that will contain issues.

    Args:
        section_ids (list[str]): List of all available section IDs.
        min_issues (int): Minimum number of sections to mark with issues.
        max_issues (int): Maximum number of sections to mark with issues.

    Returns:
        set[str]: A set of randomly selected section IDs that will contain issues.
    """

    count = random.randint(min_issues, max_issues)
    return set(random.sample(section_ids, count))


def print_section_console(
    title: str,
    content: str,
    level: int,
    parent_title: str | None
) -> None:
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


def print_injected_issues(
    issues: list[InjectedIssue],
    level: int
):
    """
    Print a list of injected issues to the console with formatting and indentation.

    Args:
        issues (list[InjectedIssue]): A list of issues to print.
        level (int): The nesting level of the parent section.
    """
    if not issues:
        return

    indent = "  " * (level - 1)
    print(f"{indent}⚠️  Injected issues:")

    for i, issue in enumerate(issues, start=1):
        sev = f" [{issue.severity}]" if issue.severity else ""
        print(f"{indent}  {i}. {issue.description}{sev}")


def assemble_sections_to_html(sections: List[Section]) -> str:
    """
    Assemble a list of cleaned sections into a single HTML string.

    Args:
        sections (List[Section]): A list of Section objects.

    Returns:
        str: A single HTML string containing all sections wrapped in `<section>` tags.
    """

    parts: list[str] = []

    for section in sections:
        # Clean and fix unclosed/malformed tags
        clean_html = BeautifulSoup(section.content_html, "html.parser")
        body = str(clean_html)

        # Wrap in section
        parts.append(
            f'<section id="{section.id}">\n{body}\n</section>'
        )

    return "\n\n".join(parts)


def generate_sections_from_toc(
    tool: Tool,
    toc: TOC,
    document_type: str,
    model: str,
    temperature: float,
    max_tokens: int,
    prompt_name: str
) -> Tuple[List[Section], List[InjectedIssue]]:
    """
    Generate structured document sections from a table of contents (TOC) using an LLM.

    Args:
        tool (Tool): The software tool object for which the document is generated
        toc (TOC): Table of contents object with `sections` to generate content for.
        document_type (str): Type of document being generated (used in prompts).
        model (str): Name of the LLM model to use for generation.
        temperature (float): Sampling temperature for the LLM.
        max_tokens (int): Maximum tokens to generate per section.
        prompt_name (str): Name of the prompt template to load.

    Returns:
        Tuple[List[Section], List[InjectedIssue]]:
            - List[Section]: Generated sections with cleaned HTML content.
            - List[InjectedIssue]: List of issues injected into sections.
    """

    generated: List[Section] = []
    collected_issues: List[InjectedIssue] = []

    # plan issues at document level
    config = load_config("config.yaml")
    section_ids = collect_section_ids(toc)
    issue_sections = get_issue_sections(
        section_ids, 
        config.issues.min_per_document, 
        config.issues.max_per_document
    )

    def clean_html(html_str: str) -> str:
        """
        Clean and fix HTML content by automatically closing unclosed tags.

        Args:
            html_str (str): A string containing HTML content that may be malformed or have unclosed tags.

        Returns:
            str: A cleaned HTML string with properly closed tags.
        """
        soup = BeautifulSoup(html_str, "html.parser")
        return str(soup)

    def walk(section: TOCSection, level: int, parent_title: str | None):
        """
        Recursively generate content for a section and its subsections using an LLM.

        For each TOC section and subsection:
        - Injects a subtle quality issue if needed.
        - Calls the LLM to generate HTML content
        - Cleans and validates html content.

        Args:
            section: A Section object to generate content for.
            level (int): The nesting level of the section for indentation and formatting.
            parent_title (str | None): The title of the parent section, if any.

        """

        has_issue = section.id in issue_sections

        issue_instruction = (
            "Include exactly ONE subtle quality issue in this section, such as typo, contradiction, inconsistent terminology or ambiguity. "
            "Choose the issue type yourself. The issue must be minor and realistic."
            if has_issue
            else
            "Do NOT introduce any inconsistencies, ambiguities, typos, or errors."
        )

        prompt = load_prompt(prompt_name).format(
            tool_name=tool.name,
            purpose=tool.purpose,
            document_type=document_type,
            section_title=section.title,
            parent_title=parent_title or "None",
            previous_summary=summarize_previous_sections(generated),
            issue_instruction=issue_instruction,
        )

        result = call_llm(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            text_format=SectionLLMOutput
        )

        result = SectionLLMOutput.model_validate(result)

        # Clean HTML and update section
        section_html = clean_html(result.content)

        # Print for debug
        print_section_console(
            title=section.title,
            content=section_html,
            level=level,
            parent_title=parent_title
        )

        # Collect issues
        for issue in result.issues:
            issue.section_id = section.id
            issue.section_title = section.title
            collected_issues.append(issue)

        print_injected_issues(result.issues, level)

        # Add to generated sections
        generated.append(
            Section(
                id=section.id,
                title=section.title,
                level=level,
                content_html=section_html,
                parent_id=section.id if parent_title else None,
            )
        )

        for child in section.subsections:
            walk(child, level + 1, section.title)

    for top in toc.sections:
        walk(top, level=1, parent_title=None)

    return generated, collected_issues