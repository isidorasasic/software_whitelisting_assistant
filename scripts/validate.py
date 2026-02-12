from html.parser import HTMLParser
from typing import Set, List
from software_whitelisting_assistant.scripts.classes import TOC, TOCSection, InjectedIssue
from software_whitelisting_assistant.scripts.load_config import load_configuration


class TOCValidationError(Exception):
    """Raised when a TOC fails structural or logical validation."""
    pass


def validate_toc(toc: TOC) -> None:
    """
    Validate the structural and logical integrity of a table of contents (TOC).

    Args:
        toc (TOC): The TOC to validate.

    Raises:
        TOCValidationError: If any validation rule is violated.
    """

    if not toc.id.strip():
        raise TOCValidationError("TOC id is empty")

    if not toc.title.strip():
        raise TOCValidationError("TOC title is empty")

    if not toc.sections:
        raise TOCValidationError("TOC has no sections")

    seen_ids: Set[str] = set()

    def walk(section: TOCSection, level: int):
        # ---- Required fields ----
        if not section.id.strip():
            raise TOCValidationError("Section id is empty")

        if not section.title.strip():
            raise TOCValidationError(f"Empty title in section '{section.id}'")

        # ---- Uniqueness ----
        if section.id in seen_ids:
            raise TOCValidationError(f"Duplicate section id: {section.id}")
        seen_ids.add(section.id)

        # ---- Recurse ----
        for child in section.subsections:
            walk(child, level + 1)

    for top_level in toc.sections:
        walk(top_level, level=1)


class HTMLValidationError(Exception):
    """Raised when generated HTML fails basic structural validation."""
    pass


class _HTMLValidator(HTMLParser):
    """
    Internal HTML parser to check basic structure.

    Tracks open tags, ensures <body> exists, and detects headings.
    Raises HTMLValidationError on mismatched or unexpected tags.
    """

    def __init__(self):
        super().__init__()
        self.open_tags = []
        self.has_body = False
        self.has_heading = False

    def handle_starttag(self, tag, attrs):
        self.open_tags.append(tag)

        if tag == "body":
            self.has_body = True

        if tag in {"h1", "h2", "h3"}:
            self.has_heading = True

    def handle_endtag(self, tag):
        if not self.open_tags:
            raise HTMLValidationError(f"Unexpected closing tag </{tag}>")

        last = self.open_tags.pop()
        if last != tag:
            raise HTMLValidationError(
                f"Mismatched tag: expected </{last}>, got </{tag}>"
            )


def validate_html(html: str) -> None:
    """
    Perform basic structural validation on a generated HTML document.

    Args:
        html (str): The HTML content to validate.

    Raises:
        HTMLValidationError: If any validation rule is violated.
    """

    if not html.strip():
        raise HTMLValidationError("HTML document is empty")

    parser = _HTMLValidator()
    parser.feed(html)

    if parser.open_tags:
        raise HTMLValidationError(
            f"Unclosed tags remain: {parser.open_tags}"
        )

    if not parser.has_body:
        raise HTMLValidationError("Missing <body> tag")

    if not parser.has_heading:
        raise HTMLValidationError("HTML contains no headings")


class InjectedIssueValidationError(Exception):
    """Raised when the number of generated issues
    is not matching the configuration parameters."""
    pass


def validate_injected_issues(injected_issues: List[InjectedIssue]):
    """
    Validate if the number of injected issue marches the config parameters.

    Args:
        injected_issues (List[InjectedIssue]): The list of InjectedIssue objects.

    Raises:
        InjectedIssueValidationError: If any validation rule is violated.
    """
    # Load configuration
    config = load_configuration()

    if len(injected_issues) < config.issues.min_per_document or \
       len(injected_issues) > config.issues.max_per_document:
        raise InjectedIssueValidationError(
            f"The number of injected issues ({len(injected_issues)}) is not matching the configuration"
        )
