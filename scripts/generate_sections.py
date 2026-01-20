# generation/section_generator.py
from typing import List, Set
from software_whitelisting_assistant.scripts.classes import Section, SectionLLMOutput, InjectedIssue
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt
import random
import json


def summarize_previous_sections(sections, limit: int = 3) -> str:
    """
    Provide lightweight context for continuity without token bloat.
    """
    if not sections:
        return "None"

    recent = sections[-limit:]
    return "\n".join(f"- {s.title}" for s in recent)


def save_issue_metadata(path, issue_sections: set[str]):
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
    min_issues: int = 2,
    max_issues: int = 3,
) -> Set[str]:
    """
    Decide which sections will contain issues.
    The LLM will decide the type of issue.
    """
    count = random.randint(min_issues, max_issues)
    return set(random.sample(section_ids, count))


def print_section_console(
    title: str,
    content: str,
    level: int,
    parent_title: str | None
) -> None:
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
) -> None:
    
    if not issues:
        return

    indent = "  " * (level - 1)
    print(f"{indent}⚠️  Injected issues:")

    for i, issue in enumerate(issues, start=1):
        sev = f" [{issue.severity}]" if issue.severity else ""
        print(f"{indent}  {i}. {issue.description}{sev}")


def generate_sections_from_toc(
    toc,
    tool,
    document_type: str,
    model: str,
    temperature: float,
    prompt_name: str
) -> List[Section]:

    generated: List[Section] = []

    # plan issues at document level
    section_ids = collect_section_ids(toc)
    issue_sections = get_issue_sections(section_ids)

    def walk(section, level: int, parent_title: str | None):

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

        # html = call_llm(
        #     prompt=prompt,
        #     model=model,
        #     temperature=temperature,
        #     max_tokens=600
        # )

        result = call_llm(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=600,
            text_format=SectionLLMOutput
        )

        result = SectionLLMOutput.model_validate(result)

        # print to console
        section.content = result.content

        print_section_console(
            title=section.title,
            content=section.content,
            level=level,
            parent_title=parent_title
        )

        # ✅ Print issues
        for issue in result.issues:
            issue.section_id = section.id
            issue.section_title = section.title

        print_injected_issues(result.issues, level)

        generated.append(
            Section(
                id=section.id,
                title=section.title,
                level=level,
                content_html=section.content,
                parent_id=section.id if parent_title else None,
            )
        )

        for child in section.subsections:
            walk(child, level + 1, section.title)

    for top in toc.sections:
        walk(top, level=1, parent_title=None)

    return generated