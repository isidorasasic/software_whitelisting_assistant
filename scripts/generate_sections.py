from typing import List, Set, Tuple, Mapping
import random
import html
from bs4 import BeautifulSoup
from software_whitelisting_assistant.scripts.classes import Tool, TOC, TOCSection, Section, SectionLLMOutput, InjectedIssue
from software_whitelisting_assistant.scripts.llm_client import call_llm
from software_whitelisting_assistant.scripts.load_config import load_configuration
from software_whitelisting_assistant.scripts.utils import print_injected_issues, print_section_console
from software_whitelisting_assistant.scripts.artifacts_store import load_prompt


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


def assemble_sections_from_toc(
    toc_sections: list[TOCSection],
    section_by_id: Mapping[str, Section], *,
    strict: bool = False
) -> str:
    """
    Render nested HTML <section> elements based on the TOC tree.
    - toc_sections: top-level TOC nodes
    - section_by_id: mapping from section id -> Section
    - strict: if True, raise KeyError when a TOC node has no matching Section;
      if False, skip it.
    """
    
    parts: list[str] = []

    def render_node(node: TOCSection) -> str:
        sec = section_by_id.get(node.id)
        if sec is None:
            if strict:
                raise KeyError(f"No Section found for TOC id '{node.id}'")
            return ""  # skip this node (and its subtree)

        inner_parts = [sec.content_html]
        for child in node.subsections or []:
            child_html = render_node(child)
            if child_html:
                inner_parts.append(child_html)

        level_attr = f' data-level="{sec.level}"' if getattr(sec, "level", None) is not None else ""
        return (
            f'<section id="{html.escape(sec.id, quote=True)}"{level_attr}>'
            + f"<h{sec.level+1}>{sec.title}</h{sec.level+1}>"
            + "\n".join(inner_parts)
            + "</section>"
        )

    for node in toc_sections:
        rendered = render_node(node)
        if rendered:
            parts.append(rendered)

    return "\n\n".join(parts)


def build_full_html(
    toc: TOC,
    sections: List[Section], *,
    strict: bool = False
) -> str:
    """
    Assemble a complete HTML document from a TOC and its sections.

    Args:
        toc (TOC): The table of contents describing the document structure.
        sections (List[Section]): The list of generated sections with HTML content.
        strict (bool, optional): If True, enforce strict HTML assembly rules.
                                 Defaults to False.

    Returns:
        str: A complete HTML document as a string.
    """
    section_by_id: Mapping[str, Section] = {s.id: s for s in sections}
    body_html = assemble_sections_from_toc(toc.sections, section_by_id, strict=strict)

    return (
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8" />
        <title>{html.escape(toc.title)}</title>
        </head>
        <body>
        {body_html}
        </body>
        </html>
        """.strip()
    )


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
    config = load_configuration()
    section_ids = collect_section_ids(toc)
    issue_sections = get_issue_sections(
        section_ids, 
        config.issues.min_per_document, 
        config.issues.max_per_document
    )

    # DEBUG
    # print("Issue sections:\n")
    # print(issue_sections)

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
            "Include exactly ONE and only ONE of the following issue types in this section: "
            "a minor typo, a minor internal contradiction, a single instance of inconsistent terminology, "
            "or a minor ambiguity. Choose ONE type only. "
            "The issue must be subtle, realistic, and limited to a single occurrence."
            if has_issue
            else
            "Write the section as a fully correct, internally consistent legal text with precise terminology."
        )

        prompt = load_prompt(prompt_name).format(
            tool_name=tool.name,
            purpose=tool.purpose,
            document_type=document_type,
            section_title=section.title,
            parent_title=parent_title or "None",
            previous_sections=generated,
            issue_instruction=issue_instruction,
        )

        # DEBUG
        # print("PROMPT:\n")
        # print(prompt)

        result = call_llm(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            text_format=SectionLLMOutput
        )

        # make sure injected issue is present
        while not result.issue and has_issue:
            # DEBUG
            # print("\nEntered second LLM call - SECTIONS\n")
            result = call_llm(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                text_format=SectionLLMOutput
            )

        # if LLM injected issue to the wrong section set it to null
        if result.issue and not has_issue:
            # DEBUG
            # print("\nLLM introduced issue to the WRONG section\n")
            # print_injected_issues(result.issue, level)
            result.issue = None

        result = SectionLLMOutput.model_validate(result)

        # Clean HTML and update section
        section_html = clean_html(result.content)
        
        print_section_console(
            title=section.title,
            content=section_html,
            level=level,
            parent_title=parent_title
        )

        # Collect issues
        collected_issues.append(result.issue)

        print_injected_issues(result.issue, level)

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

    # clean the issue list from None
    collected_issues = [issue for issue in collected_issues if issue]

    return generated, collected_issues