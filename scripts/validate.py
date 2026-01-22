from html.parser import HTMLParser
from typing import Set
from software_whitelisting_assistant.scripts.classes import TOC, TOCSection


class TOCValidationError(Exception):
    pass


def validate_toc(toc: TOC) -> None:
    """
    Validates structural and logical integrity of a TOC.
    Raises TOCValidationError if invalid.
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
    pass


class _HTMLValidator(HTMLParser):

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
    Basic structural validation for generated HTML.
    Raises HTMLValidationError if invalid.
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

